# Unraveling the connections between actors and character tropes in movies

*Abstract*

In the movie industry, creativity is generally considered to be a key to success. In particular, actors need to keep reinventing themselves to keep the audience engaged. Conversely, if critics praise an actor's performance, it would be wise to keep playing roles that are similar to the acclaimed performance. What is the correct strategy for an actor ? Are there roles which are acclaimed only when they are played by a group of actors ? Our goal is to answer those questions with data analysis. Especially, we want to explore the connections between actors and character tropes in movies. First, we will focus on actors that tend to play the same character across movies. Do they represent a big proportion of the actors ? Does this role guarantee the movie's success ?
Then, we will analyse if a given character trope matches certain actor features. Does the ethnicity of an actor impact the distribution of his roles ?

## Structure of the repository

The following diagram presents the structure of this repository :
```
├───data
│   ├───cmu
│   │   ├───MovieSummaries
│   │   └───personas
│   ├───imdb
│   └───wikidata
└───src
    ├───analysis
    └───preprocessing
```

<!-- The `data` folder contains the `cmu` and `imdb` datasets. In order to merge these datasets, we require a third one, specifically the `wikidata` dataset. The dataset contains a `.json` file that provides the Freebase ID and IMDb ID for each movie. -->

First in order to download all required dataset, run the `download_dataset.py` from the root repository (may take a while)
```
python ./src/preprocessing/download_dataset.py
```

<!-- To load the datasets, run the `load_dataset.py` from the root of the repository:
```
py .\src\preprocessing\load_dataset.py
``` -->

## Research questions

1. What is the proportion of actors that tend to play the same type of character across movies ?
2. To what extent does the fact that an actor plays roles outside his comfort zone determine the success of his movies ?
3. Are there roles that are acclaimed only when they are played by a specific group of actors ?
4. Does the ethnicity of an actor impact the distribution of his roles ?

## Data Acquisition

Our question revolves around actors, their *associated* personas and how well this *association* influences the success of a film. To that end, we need to define a metric of "success" of a film, even if we are already provided with the `box_office` column in the cmu dataset, it only include the bigger blockbusters (in itself a source of bias). We have therefore decided to use the imdb rating of the film as a metric defining the success of the film.

> Note: As a possible extension, we could use a sentiment analysis algorithm on imdb's review dataset in order to retrieve a distribution of sentiment. This could enable us to define a more refined metric than simply the average (`stddev + median`, `q05 + q95`, ...)

## Pipeline

1. Retrieve actors persona distribution :

   During this stage, we `group` all **characters** accross all films by **actors**. For each *characters* we retrieve the corresponding *personas* (as defined in the `cmu` dataset). This enables us to extract the distribution of persona for each **actors**. We then filter all **actors** playing more than a certain threshold $K$ personas (cannot deduce anything from an actor who played in only $2$ movies).

2. Retrieve global persona distribution :

   In order to make comparaison about *actors personas*, we need to compare it to the global persona distribution. To do so, we need to extract this global persona distribution

   > Note : We must ensure that the global distribution of personas is computed accross all actors with at least $K$ personas.

3. Define a `preference metric` for each actors :

   To determine to what extent a given actor $A$ prefer playing a certain persona, we need to metric to quantify this preference. Here are a list of proposed metric

   - `Cross Entropy`:
      $$ 
         f(\text{Actor}) = \frac{ H(\text{Persona}) }{ H(\text{Persona} | \text{Actor}) }
      $$

      This metric has the following property
      - If the actor $A$ always plays the same persona, then $f(A) = +\inf$
      - If the actor $A$ plays each persona randomly (same distribution than the global distribution), then $f(A) = 1$

      > Note that this metric is not well-behaved as it is not bounded. We can take the inverse to keep a value between 0 and 1, the value 1 would mean that $A$ plays each persona randomly and 0 would mean that $A$ keeps playing the same persona
   
   - `Mutual Information`:
      $$
         f(\text{Actor}) = \frac{I(\text{Persona}, \text{Actor})}{H(\text{Persona})} = \frac{ H(\text{Persona}) - H(\text{Persona} | \text{Actor}) }{H(\text{Persona})}
      $$

      This metric has the following property
      - If the actor $A$ always plays the same persona, then $f(A) = 1$
      - If the actor $A$ plays each persona randomly (same distribution than the global distribution), then $f(A) = 0$
        
4. Define a `likelihood metric` for each actors :

   To determine how likely a given actor $A$ is to play a persona $P$, we need a metric to estimate $P(P | A)$. The empirical probability can be used to estimate this likelihood

5. We can then try to find if there are a correlation between metric defined in step `3.` and step `4.` and the success of the film defined in step `1.`

<!-- We can group all `characters` by `actors` -->

## Possible overlooked bias

This approach, even though still relatively simple, overlooked some major bias that could lead to unfounded result.

 - Impact of player *fame* :

   Assume that a given actor $A$ have a high preference for a persona $P$. Movies he played a persona $P' \neq P$ tend to under-performed compare to the other movies. This could be explain by the fact that most movie he played as $P'$, were before this actor was "famous" and as such he was playing roles in film with much smaller franchise. When he/her became famous, he could take the luxury to decide whether he wanted to play as $P'$ or not.

   <!-- TODO:  Solution ? -->

   ```mermaid
   graph TD;
      A(Fame)-->B(Persona);
      B-->C(Movie Success);
      A-->C;
   ```
