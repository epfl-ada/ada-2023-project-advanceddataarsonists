# Unraveling the connections between actors and character tropes in movies
In this project we want to explore the connections between actors and character tropes in movies. First, we will focus on actors that tend to play the same character accross movies. Do they represent a big proportion of the actors ? Does this role guarantee the movie's success ?  
Then, we will analyse if a given character trope matches certain actor features. Does the ethnicity of an actor impact the distribution of his roles ?

## Structure of the repository

The following diagram presents the structure of this repository :
```
├───data
│   ├───cmu
│   └───imdb
│       ├───title.akas.tsv
│       ├───title.basics.tsv
│       ├───title.crew.tsv
│       ├───title.episode.tsv
│       ├───title.principals.tsv
│       └───title.ratings.tsv
├───src
│   └───preprocessing
```
Note that the `dataset/` folder is empty as the CMU dataset is too voluminous to fit in a GitHub repository. The `dataset/` must contain the `.tsv` and `.txt` files of the CMU movies dataset.
