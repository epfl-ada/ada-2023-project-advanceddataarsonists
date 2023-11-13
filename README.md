# Unraveling the connections between actors and characters in movies

## Abstract

In the movie industry, creativity is generally considered to be a key factor in the success of a film. Actors often need to reinvent themselves to keep audiences hooked, but do they really ? Some actors tend to develop a comfort zone and keep playing the same type of movies/characters. Our projects aims at discovering those comfort zones, when they are created and what happens when an actors steps out of it. Conversly, we also want to evaluate if a given role/character tends to be played only by a subset of actors and which feature(s) do these actors share, which could lead us to uncover racial or gender biases in film castings. We use the results of the [original paper](http://www.cs.cmu.edu/~ark/personas/) in order to identify in a more fine-grained approach if an actors exhibit a recurring persona accross the characters they play.

## Research questions

1. What is the proportion of actors that tend to play the same type of movies ?
2. When did an actor start to play in similar movies/a similar character ?
3. Do actors exhibit a recurring persona accross the characters they play ?
4. Is there a clear distribution shift in the perfromance of a movie when this actor is/isn't in his comfort zone ?
5. Are there roles that are acclaimed only when they are played by a specific group of actors ?
6. Which features of an actor impact the distribution of his roles ?

## Datasets

In order to download all required dataset, run the `download_dataset.py` from the root repository (may take a while)
```
python ./src/preprocessing/download_dataset.py
```

### IMDb dataset to determine movie's success

Our question revolves around actors, their *associated* personas and how well this *association* influences the success of a film. To that end, we need to define a metric of "success" of a film, even if we are already provided with the `box_office` column in the cmu dataset, it only include data for the bigger blockbusters. We have therefore decided to use the imdb rating of the film as a metric defining its performance.

We also used the `people` and `principals` collections from IMDb to enrich the `characters` collection from the CMU corpus, reducing the amount of missing information.

### WikiData translation to merge datasets

To merge movies in different datasets (CMU and IMDb), we need a third dataset that contains an ID for the CMU dataset (either freebase_id or wiki_movie_id) and the ID for the IMDb dataset (tconst). This can be done using the WikiData database. To retrieve those indices, we use the [WikiData Query service](https://query.wikidata.org/).

### TVTropes tropes

We downloaded a dataset of 500 highly curated tropes with corresponding characters from [TVTropes](https://tvtropes.org/) hoping to enrich our personas data.

### Implementation
We have written a [script](src/preprocessing/download_dataset.py) that automatically downloads all the above data from the various sources. It also contains the specific query that we make to wikidata to recover the translation between unique identifiers. The data is manageable in size and all filtering and merging steps necessary are done in Part I of the [notebook](initial_analyses.ipynb).
## Methods

## Proposed timeline

## Organization

# BELOW IS OLD METHODS SECTION THAT HAS TO BE SHORTENED/MOVED
## Methods

1. Retrieve actors persona distribution :

   During this stage, we group all **characters** accross all films by **actors**. For each **characters** we retrieve the corresponding **personas** (as defined in the `cmu` dataset). This enables us to extract the distribution of persona for each **actors**. We then filter all **actors** playing more than a certain threshold $K$ personas.

2. Retrieve global persona distribution :

   In order to make comparaison about **actors personas**, we need to compare it to the global persona distribution. To do so, we need to extract this global persona distribution

   > Note : We must ensure that the global distribution of personas is computed accross all actors with at least $K$ personas.

3. Define a **preference metric** for each actors :

   To determine to what extent a given actor $A$ prefer playing a certain persona, we need to metric to quantify this preference. Here are a list of proposed metric

   - **Cross Entropy**: $$f(\text{Actor}) = \frac{ H(\text{Persona}) }{ H(\text{Persona} | \text{Actor})}$$

      This metric has the following property
      - If the actor $A$ always plays the same persona, then $f(A) = +\infty$
      - If the actor $A$ plays each persona randomly (same distribution than the global distribution), then $f(A) = 1$

      > Note that this metric is not well-behaved as it is not bounded. We can take the inverse to keep a value between 0 and 1, the value 1 would mean that $A$ plays each persona randomly and 0 would mean that $A$ keeps playing the same persona
   
   - Mutual Information: $$f(\text{Actor}) = \frac{I(\text{Persona}, \text{Actor})}{H(\text{Persona})} = \frac{ H(\text{Persona}) - H(\text{Persona} | \text{Actor}) }{H(\text{Persona})}$$

      This metric has the following property
      - If the actor $A$ always plays the same persona, then $f(A) = 1$
      - If the actor $A$ plays each persona randomly (same distribution than the global distribution), then $f(A) = 0$
        
4. Define a **likelihood metric** for each actors :

   To determine how likely a given actor $A$ is to play a persona $P$, we need a metric to estimate $P(P | A)$. The empirical probability can be used to estimate this likelihood


5. Aggregate **preference metric** and **likelihood metric** for a given movie :  
   
   As we want to predict the success of a movie, we need to aggregate the metrics defined earlier for each actor who plays in the movie. Let's say that a movie is played by a set of actors $A = \{a_1, a_2, \dots a_n\}$ who play personas $P = \{p_1, p_2, \dots p_n\}$ (where $a_i$ plays persona $p_i$). Let's call the `preference metric` $\text{pref}(a)$ and the likelihood metric $\text{like}(a, p)$ (for $a \in A$ and $p \in P$). We propose the following aggregation strategies :
   - Mean/median over both metrics
   - Weighted average on the "importance" of the roles of the actor (where actors who play a more important role in the movie will have a higher weight)

     > How do we get the "importance of the role" ?
   - Random sampling
   This aggregation gives us a `preference metric` and a `likelihood metric` on the movie $m$ that we can use later for the analysis part [we call them $\text{pref}(m)$ and $\text{like}(m)$].

6. Modelisation of our project question

   - Naïve model :

     We can then try to find if there are a correlation between $(\text{pref}(m), \text{like}(m))$ and the success of the film defined in step `1.`. A naïve approach would be to estimate the *p-value* of the hypothesis $H_0$ defined as **"The probability that both metrics and the success of the film is uncorrelated"**. We could then try to build a confidence interval on the correlation metric (Pearson's correlation coefficient).

   - Causal analysis :
     
     To determine if the movie's success is driven by the fact that an actor played a role outside of his comfort zone, we can use $\text{pref}(m)$ and $\text{like}(m)$. We first cluster movies in different groups according to their $\text{pref}(m)$ and $\text{like}(m)$ (movies with similar metrics should be clustered in the same group). Algorithms such as :
     
     - K-means clustering
     - Fisher LDA
     can be used to cluster similar movies.

     Then for a given movie, we use as many covariates as we can (budget, genre, release date, ...) and the two metrics mentioned before on all of the actors. The metric of step `4.` is used for the actor and the persona played by the actor for the movie.

   - Hypothesis Testing :
     
     Interpreting our metrics as features to determine the film.

   - *Draw beautiful graph*

`Note :` Both metric `2.` and `3.` are required together in order to differentiate between actors without any preferences playing a role that is rare against
   actors with a clear preferences playing a persona outside of their comfort zone.

<!-- We can group all `characters` by `actors` -->

### Possible bias and Limitations

> Those are possibles biases and limitations that the previously described naive model can suffer from.

This approach, even though still relatively simple, overlooked some major bias that could lead to unfounded result.

 - Actor *fame* as a confounder :

   Assume that a given actor $A$ have a high preference for a persona $P$. Movies he played a persona $P' \neq P$ tend to under-performed compare to the other movies. This could be explain by the fact that most movie he played as $P'$, were before this actor was "famous" and as such he was playing roles in film with much smaller franchise. When he/her became famous, he could take the luxury to decide whether he wanted to play as $P'$ or not.

   ```mermaid
   graph TD
      A(Fame) --> B(Persona)
      B --> C(Movie Success)
      A --> C
   ```

   **Possible Solution** :

   > Based on the assumption that actors *fame* came with time
   
   - Add a threshold $\alpha$ and only consider movies for actors that have already played in $K \geq \alpha$ movies previously (drop first $\alpha - 1$ movies for 
   each actors)
      
   - Add a third metric $R$ to our model defined as $$R(\text{Actor}, \text{Movie}) = \frac{\text{Number of movies played by actor A prior to M}}{\text{Number of movies played by actor A}}$$

     This would be able to distinguish between the case where $R < \alpha$ and $R > \alpha$ for a given $\alpha$. We could also try to evaluate the strength of this bias by testing the model *with* and *without* this metric. Notice that this is just an extension of the previously defined method. However this extension is more polyvalent than the previos method.
   
 - Impact of certain *personas* onto the overall film :

   We could imagine a scenario where the presence of a persona $P$ in our film has a possive effect on the success of this film. As such our model may conclude that actors that have a preference for persona $P$ playing as $P$ as a better effect on the movie success that if he were playing as $P'$ instead.

   **Possible Solution** :

   - Instead of comparing actors that play in their preferred role or not, we should compare how much better an actor playing in his preferred persona
     will improve the movie compared to another actor without particular preference (Let us called this actor the *neutral actor*). We can therefore either
     perform

     - A difference in difference of means between the both (where *neutral actors* are defined by a certain threshold $\alpha$ defined on the metric `1.`).
   

     - Matching between *neutral actors* and *actors* with a preferrence (however this may end up being complexify by the limited amount)
