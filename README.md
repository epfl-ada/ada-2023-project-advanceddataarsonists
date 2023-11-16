# Unraveling the connections between actors and characters in movies

## Abstract

In the movie industry, creativity is generally considered to be a key factor in the success of a film. Actors often need to reinvent themselves to keep audiences hooked, but do they really ? Some actors tend to develop a comfort zone and keep playing the same type of movies / characters. Our projects aims at discovering those comfort zones, when they are created and what happens when actors step out of it. Conversly, we also want to evaluate if a given role/character tends to be played only by a subset of actors and which feature/s these actors share, which could lead us to uncover racial or gender biases in film castings. We build on top of the results of the [original paper](http://www.cs.cmu.edu/~ark/personas/) in order to identify in a more fine-grained approach if an actors exhibit a recurring persona accross the characters they play.

## Research questions

1. What is the proportion of actors that tend to play the same type of movies ?
2. When did an actor start to play in similar movies/similar characters ?
3. Do actors exhibit a recurring persona accross the characters they play ?
4. Is there a clear distribution shift in the perfromance of a movie when this actor is/isn't in his comfort zone ?
5. Are there roles that are acclaimed only when they are played by a specific group of actors ?
6. Which features of an actor impact the distribution of his roles ?

## Datasets

In order to download all required datasets, run the [download_dataset.py](src/preprocessing/download_dataset.py) from the root repository (may take a while)
```
python ./src/preprocessing/download_dataset.py
```

### IMDb

We need to define a metric of "success" of a film. Even if we are already provided with the `box_office` column in the cmu dataset, it only includes data for the bigger blockbusters, which represent only 10% of the movies. We have therefore decided to use the imdb rating of the film as a metric defining its performance.

We also used the `people` and `principals` collections from IMDb to enrich the `characters` collection from the CMU corpus, reducing the amount of missing information.

### WikiData

To merge movies from different sources (CMU and IMDb), we need a translation layer that contains an ID for the CMU dataset (either freebase_id or wiki_movie_id) and for the IMDb dataset (tconst). This can be done by querying the WikiData database using [WikiData Query service](https://query.wikidata.org/).

### TVTropes tropes

We downloaded a dataset of 500 highly curated tropes with corresponding characters from [TVTropes](https://tvtropes.org/) to enrich our personas data.

## Methods

We divide our data analysis pipeline into XXX parts.

### Part I - Refining the movie dataset and enriching characters
The first step of our data analysis pipeline is dedicated to the creation of two collections: (1) movies with ratings and optional summaries and (2) movie characters and corresponding actors.  
As stated above, we need a way of measuring the performance of a movie. To do so we chose to enrich the CMU movies with ratings from IMDb and use mean rating as a metric. Once this collection is created, we filter CMU characters to keep the ones appearing in those movies. We use IMDb actor and character data to enrich the CMU collection by filling missing values for character names and actor features.

### Part II - Adding character tropes
The second step is dedicated to character tropes. In order to determine if an actor exhibits a reccurring persona accross his characters we introduce two possible metrics that measure to what extent an actor prefers playing a certain persona:  
(1) The **cross entropy metric** which computes the entropy of persona choices given the actor $$f(\text{Actor}) = \frac{ H(\text{Persona}) }{ H(\text{Persona} | \text{Actor})}$$  
(2) the **mutual information metric** which captures the information gain about the actor's persona choices relative to the global persona distribution $$f(\text{Actor}) = \frac{I(\text{Persona}, \text{Actor})}{H(\text{Persona})} = \frac{ H(\text{Persona}) - H(\text{Persona} | \text{Actor}) }{H(\text{Persona})}$$  
Properties and examples of application of those metrics are provided in the notebook.

***
1. Retrieve Actors' Persona and Movies' Genre Distribution:

   Group all characters across all movies by **actors**.
   For each **characters**, retrieve the corresponding personas and movie genres (as defined in the `cmu` dataset).
   This enables the extraction of the distribution of personas and movie genres for each actor, Then we filter out **actors** playing more than a certain threshold of personas or genres.

2. Retrieve global persona distribution :

   Extract the global persona and genre distribution to enable comparisons.
   > Note :The global distribution of personas and genres is computed across all actors with at least a certain threshold of personas or genres.

3. Define a **preference metric** for each actors :

   To determine to what extent a given actor $A$ plays diverse roles or not, we need to metric to quantify this preference. Here are a list of proposed metric

   - **Cross Entropy**: 
   
   The Cross Entropy Metric focuses on the entropy of persona choices given the actor
   $$\text{pref}(\text{actor}) = \frac{ H(\text{Persona}) }{ H(\text{Persona} | \text{Actor} = \text{actor})}$$

      This metric has the following property
      - If the actor $a$ always plays the same persona, then $\text{pref}(a) = +\infty$
      - If the actor $a$ plays each persona randomly (same distribution than the global distribution), then $\text{pref}(a) = 1$

      > Note that this metric is not well-behaved as it is not bounded. We can take the inverse to keep a value between 0 and 1, the value 1 would mean that $A$ plays each persona randomly and 0 would mean that $A$ keeps playing the same persona
   
   - **Mutual Information**: 
   
   Mutual Information Metric captures the information gain about the actor's persona choices relative to the global persona distribution
   $$\text{pref}(\text{actor}) = \frac{ H(\text{Persona}) - H(\text{Persona} | \text{Actor} = \text{actor}) }{H(\text{Persona})}$$
      
      This metric has the following property
      - If the actor $a$ always plays the same persona, then $\text{pref}(a) = 1$
      - If the actor $a$ plays each persona randomly (same distribution than the global distribution), then $\text{pref}(a) = 0$

      >Both metrics offer insights into the diversity or consistency of an actor's persona preferences.
        

4. Define a **likelihood metric** for each actors :

   To determine how likely a given actor $A$ is to play a persona $P$ or in a specific movie genre, we need a metric to estimate both of $P(\text{Persona} | \text{Actor} = \text{a})$ and $P(\text{MovieGenre} | \text{Actor} = \text{a})$. The empirical probability can be used to estimate this likelihood


5. Aggregate **preference metric** and **likelihood metric** for a given movie :  
   
   As we want to predict the success of a movie, we need to aggregate the metrics defined earlier for each actor who plays in the movie.  We propose the following aggregation strategies :
   - Mean/median over both metrics
   - Weighted average on the "importance" of the roles of the actor (where actors who play a more important role in the movie will have a higher weight)

     > How do we get the "importance of the role" ?
   - Random sampling
   This aggregation gives us a `preference metric` and a `likelihood metric` on the movie $m$ that we can use later for the analysis part [we call them $\text{pref}(m)$ and $\text{like}(m)$].

`Note :` Both metric $\text{like}$ and $\text{pref}$ are required together in order to differentiate between actors without any preferences playing a role that is rare against actors with a clear preferences playing a persona outside of their comfort zone.

### Part III : Modelisation of our project question

To determine if actors' preferences influence the success of a movie we will explore the following ideas :

   - Naïve model :

     We can then try to find if there are a correlation between $(\text{pref}(m), \text{like}(m))$ and the success of the film defined in step `1.`. A naïve approach would be to estimate the *p-value* of the hypothesis $H_0$ defined as **"The probability that both metrics and the success of the film is uncorrelated"**. We could then try to build a confidence interval on the correlation metric (Pearson's correlation coefficient).

   - Causal analysis :
     
     To determine if the movie's success is driven by the fact that an actor played a role outside of his comfort zone, we can use $\text{pref}(m)$ and $\text{like}(m)$. We first cluster movies in different groups according to their $\text{pref}(m)$ and $\text{like}(m)$ (movies with similar metrics should be clustered in the same group). Algorithms such as :
     
     - K-means clustering
     - Fisher LDA
     can be used to cluster similar movies.

     Then for a given movie, we use as many covariates as we can (budget, genre, release date, ...) and the two metrics mentioned before on all of the actors. The metric of step `4.` is used for the actor and the persona played by the actor for the movie.



## Proposed timeline

| Date | Goal |
|-|-|
| 3 Nov 2023 | In depth CMU data exploration, data cleaning, preprocessing |
| 10 Nov 2023 | Enriching dataset with IMDB and TVTropes , visualisation of different distributions, initial analysis  |
| 17 Nov 2023 | **Milestone 2 deadline**  |
| 24 Nov 2023 | Start working on the project model , focus on Homework 2|
| 01 Dec 2023 | **Homework 2 deadline** |
| 08 Dec 2023 | Provide detailed analysis for each research question |
| 15 Dec 2023 | Finalize code implementations, Draft of the final datastory |
| 20 Dec 2023 | Create all visualizations for datastory and complete final text |
| 22 Dec 2023 | **Milestone 3 deadline** |

