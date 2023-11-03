# Unraveling the connections between actors and character tropes in movies
In this project we want to explore the connections between actors and character tropes in movies. First, we will focus on actors that tend to play the same character accross movies. Do they represent a big proportion of the actors ? Does this role guarantee the movie's success ?  
Then, we will analyse if a given character trope matches certain actor features. Does the ethnicity of an actor impact the distribution of his roles ?

## Structure of the repository

The following diagram presents the structure of this repository :
```
├───data
│   ├───cmu
│   │   └───MovieSummaries
│   ├───imdb
│   └───wikidata
└───src
    └───preprocessing
```

The `data` folder contains the `cmu` and `imdb` datasets. In order to merge these datasets, we require a third one, specifically the `wikidata` dataset. The dataset contains a `.json` file that provides the Freebase ID and IMDb ID for each movie.

To load the datasets, run the `load_dataset.py` from the root of the repository:
```
py .\src\preprocessing\load_dataset.py
```

## Pipeline

### Datasets loading

## Methods