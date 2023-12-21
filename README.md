# Unraveling the connections between actors and characters in movies

## Data story

Uncover the mystery behind actors' success [here](https://michelducartier.github.io/ada-jekyll)! 

## Abstract

In the movie industry, creativity is generally considered to be a key factor in the success of a film. Actors often need to reinvent themselves to keep audiences hooked, but do they really ? Some actors tend to develop a comfort zone and keep playing the same type of movies / characters. Our projects aims at discovering those comfort zones, when they are created and what happens when actors step out of it. Conversly, we also want to evaluate if a given role/character tends to be played only by a subset of actors and which feature/s these actors share, which could lead us to uncover racial or gender biases in film castings. We build on top of the results of the [original paper](http://www.cs.CMU.edu/~ark/personas/) in order to identify in a more fine-grained approach if an actors exhibit a recurring persona accross the characters they play.

## Research questions

1. What is the proportion of actors that tend to play the same type of movies ?
2. When did an actor start to play in similar movies/similar characters ?
3. Do actors exhibit a recurring persona accross the characters they play ?
4. Is there a clear distribution shift in the performance of a movie when this actor is/isn't in his comfort zone ?
5. Are there roles that are acclaimed only when they are played by a specific group of actors ?
6. Which features of an actor impact the distribution of his roles ?

## Datasets

In order to download all required datasets, run the [download_dataset.py](src/preprocessing/download_dataset.py) from the root repository (may take a while)
```
python ./src/preprocessing/download_dataset.py
```

### IMDb

We need to define a metric of "success" of a film. Even if we are already provided with the `box_office` column in the CMU dataset, it only includes data for the bigger movies, which represent only 10% of the movies. We have therefore decided to use the IMDb rating of the film as a metric defining its performance.

We also used the `people` and `principals` collections from IMDb to enrich the `characters` collection from the CMU corpus, reducing the amount of missing information.

### WikiData

To merge movies from different sources (CMU and IMDb), we need a translation layer that contains an ID for the CMU dataset (either freebase_id or wiki_movie_id) and for the IMDb dataset (tconst). This can be done by querying the WikiData database using [WikiData Query service](https://query.wikidata.org/).

### TVTropes tropes

We downloaded a dataset of 500 highly curated tropes with corresponding characters from [TVTropes](https://tvtropes.org/) to enrich our personas data.

## Methods

We divide our data analysis pipeline into 4 parts.

### Part I - Refining the movie dataset and enriching characters
The first step of our data analysis pipeline is dedicated to the creation of two collections: (1) movies with ratings and optional summaries and (2) movie characters and corresponding actors.  
As stated above, we need a way of measuring the performance of a movie. To do so we chose to enrich the CMU movies with ratings from IMDb and use mean rating as a metric. Once this collection is created, we filter CMU characters to keep the ones appearing in those movies. We use IMDb actor and character data to enrich the CMU collection by filling missing values for character names and actor features.

### Part II - Character tropes and metrics definition
The second step is dedicated to character tropes. In order to determine if an actor exhibits a reccurring persona accross his characters we introduce two possible metrics that measure to what extent an actor prefers playing a certain persona:  

(1) the **mutual information metric** which captures the information gain about the actor's persona choices relative to the global persona distribution $$pref(\text{actor}) = \frac{ H(\text{Persona}) - H(\text{Persona} | \text{Actor} = \text{actor}) }{H(\text{Persona})}$$  
Properties and examples of application of those metrics are provided in the notebook. The chosen metric is called `pref`.  


We also introduce a metric called `like` to determine how likely a given actor is to play a given persona. The empirical probability can be used to estimate this likelihood: $P(\text{Persona} | \text{Actor} = \text{a})$  

To this end, we use a variant of KL divergence to measure the difference of distribution between the current genre distribution of the current movie and the prior distribution for a given actor. More specifically given and actor $a \in A$ and a role $r \in R$. We define our `like` metric has

$$
   \text{like}(a, r) = \sum_{i=1}^N \sum_{x\in\{0,1\}} p(P_i = x | R = r) \log \left( \frac{p(P_i = x | R = r)}{p(P_i = x | A = a)} \right)
$$

As we want to analyze how both metrics relate to the success of a movie, we need to aggregate them for each actor who plays in a given movie.  We propose the following aggregation strategies:
- Mean/median over both metrics
- Weighted average on the "importance" of the roles of the actor using IMDb `knowForTitles` data.


> Note : Both metric $\text{like}$ and $\text{pref}$ are required together in order to differentiate between actors without any preferences playing a role that is rare against actors with a clear preferences playing a persona outside of their comfort zone.

### Part III - Adding movie based comfort zones
The third step is dedicated to the computation of comfort zones based on movie genre. For each actor, we have aggregated all movie data and computed a frequency vector of genres. Each element of the vector reflects the fraction of movies of a given genre that the actor played. The genre labels are saved separately. The resulting vector is added as a new column to our collection of movies characters and corresponding actors.

### Part IV - Causal analysis and clustering

To determine if actors' preferences influence the success of a movie we will perform a causal analysis :
     
We first cluster movies in 2 groups according to the parameters that we want to study (movies with similar parameters should be clustered in the same group). Algorithms such as :

   - K-means clustering
   - Fisher LDA

can be used to cluster similar movies.
As an example, those 2 groups could represent: (1) actors who played in the movie stepped out of their comfort zone or (2) they did not. Those 2 groups are analguous to the treated/control groups for causal analysis. Then we can use the methods seen in class such as matching with propensity scores to mitigate unseen correlation, and sensitivity analysis to quantify our uncertainty.

> Note : This pipeline can be extended to other parameters than personas such as genres, ethnicities and movie genres.

## Proposed timeline

| Date | Goal |
|-|-|
| 27 Oct 2023 - 17 Nov 2023 | Execute parts I to III  |
| 17 Nov 2023 | **Milestone 2 deadline**  |
| 17 Nov 2023 - 01 Dec 2023 | Homework 2 |
| 01 Dec 2023 | **Homework 2 deadline** |
| 01 Dec 2023 - 08 Dec 2023 | Create visual and compute collection statistics to answer research questions 1, 2 and 3 |
| 08 Dec 2023 - 15 Dec 2023 | Perform causal analysis to answer research questions 4, 5 and 6. Draft datastory. |
| 15 Dec 2023 | Complete draft of the final datastory |
| 15 Dec 2023 - 20 Dec 2023 | Generate and incorporate visualizations to support the datastory |
| 20 Dec 2023 - 22 Dec 2023 | Polishing steps: clean up repository, complete code comments, ensure reproducibility |
| 22 Dec 2023 | **Milestone 3 deadline** |

## Organization within the team for P2

| Teammate | Contributions |
|-|-|
| Fares | CMU and IMDb initial exploration<br/>WikiData translation data retrieval<br/>Refine README <br/> Analysis of movies' success with actors' characteristics |
| Guillaume | Automate dataset retrieval <br/> WikiData translation data retrieval <br/> Provide helper python file to load datasets <br/> Come up with `pref` and `like` metrics <br/> Causal analysis on actors personas and movie genres |
| Luca | CMU and IMDb data detailed exploration and joining steps <br/> Explore movie base comfort zones and generate genre frequency vectors <br/> Notebook overhaul <br/> Refine and complete README <br/> Causal analysis on actors personas and movie genres <br/> Data story |
| Michael | Draft of README <br/> WikiData translation data retrieval <br/> Run CMU persona pipeline <br/> Come up with `pref` and `like` metrics <br/> Refine and complete README <br/> Data story |
| Syrine | Initial data exploration <br/> TVTropes dataset exploration <br/> Data story |
