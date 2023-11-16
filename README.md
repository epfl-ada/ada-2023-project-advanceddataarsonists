﻿# Unraveling the connections between actors and characters in movies

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

   To determine to what extent a given actor $A$ plays diverse roles or not, we need to metric to quantify this preference. We need some ways to compute a preference metric from a given distribution of played personas by an actor. This metric would quantify by how much his roles are different from the global distribution of roles. For instance, this metric could take high value if the actor plays personas that nobody else play and low value if his roles follow the general distribution of personas.        

4. Define a **likelihood metric** for each actors :

   To determine how likely a given actor $A$ is to play a persona $P$ or in a specific movie genre, we need a metric to estimate both of $P(\text{Persona} | \text{Actor} = \text{a})$ and $P(\text{MovieGenre} | \text{Actor} = \text{a})$. The empirical probability can be used to estimate this likelihood


5. Aggregate **preference metric** and **likelihood metric** for a given movie :  
   
   As we want to predict the success of a movie, we need to aggregate the metrics defined earlier for each actor who plays in the movie.  We propose the following aggregation strategies :
   - Mean/median over both metrics
   - Weighted average on the "importance" of the roles of the actor (where actors who play a more important role in the movie will have a higher weight). This can be done using the "knownForTitles" column of the names basics dataframe. This column contains the principal roles of an actor. We can thus assume that those roles have a significant impact on their corresponding movies.

   - Random sampling
   This aggregation gives us a `preference metric` and a `likelihood metric` on the movie $m$ that we can use later for the analysis part [we call them $\text{pref}(m)$ and $\text{like}(m)$].

> Note : Both metric $\text{like}$ and $\text{pref}$ are required together in order to differentiate between actors without any preferences playing a role that is rare against actors with a clear preferences playing a persona outside of their comfort zone.

### Part III : Modelisation of our project question

To determine if some parameters (such as actors' preferences, movies' genres or actors' attributes) influence the success of a movie we will perform a causal analysis :
     
We first cluster movies in 2 groups according to the parameters that we want to study (movies with similar parameters should be clustered in the same group). Algorithms such as :

   - K-means clustering
   - Fisher LDA

can be used to cluster similar movies.
For example, those 2 groups can represent if actors who played in the movie stepped out of their comfort zone or not. Those 2 groups are analguous to the treated/control groups for causal analysis. Then we can use the methods seen in class such as matching with propensity scores to mitigate unseen correlation, and sensitivity analysis to quantify our uncertainty.

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

