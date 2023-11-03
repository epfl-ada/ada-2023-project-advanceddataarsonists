import pandas as pd
import os
import json

CMU_DATASET_PATH = "data/cmu/MovieSummaries"
CHARACTER_METADATA = "character.metadata.tsv"
MOVIE_METADATA = "movie.metadata.tsv"
PLOT_SUMMARIES = "plot_summaries.txt"
TVTROPES_CLUSTERS = "tvtropes.clusters.txt"

IMDB_PATH = "data/imdb/"
IMDB_REVIEWS_METADATA = "title.ratings.tsv"
IMDB_BASICS_METADATA = "title.basics.tsv"   # move to load_dataset file 
IMDB_CREW_METADATA = "title.crew.tsv"
IMDB_AKAS_METADATA = "title.akas.tsv"
IMDB_EPISODE_METADATA = "title.episode.tsv"
IMDB_PRINCIPAL_METADATA = "title.principals.tsv"

WIKIDATA_PATH = "data/wikidata/"
WIKIDATA_TRANSLATION_ID = "id-translation.wikidata.json"

characters_label = ['wiki_movie_id', 'freebase_movie_id', 'release_date', 'character_name', 'actor_birth', 
                    'actor_gender', 'actor_height', 'actor_ethnicity', 'actor_name', 'release_actor_age', 
                    'freebase_map_id', 'freebase_character_id', 'freebase_actor_id']

movies_label = ['wiki_movie_id', 'freebase_movie_id', 'movie_name', 'movie_release_date', 'box_office',
               'movie_runtime', 'movie_languages', 'movie_countries', 'movie_genres']

plot_label = ['wiki_movie_id', 'plot_summary']

tvtropes_label = ['trope_name', 'character_data']

def load_translation_df():
    with open(os.path.join(WIKIDATA_PATH, WIKIDATA_TRANSLATION_ID)) as file:
        raw_table = json.load(file)

    imdb_id = []
    freebase_id = []

    for robject in raw_table['results']['bindings']:
        imdb_id.append(robject['IMDb_ID']['value'])
        freebase_id.append(robject['freebase_id']['value'])

    return pd.DataFrame(data={ 'imdb_id': imdb_id, 'freebase_id': freebase_id })

def load_characters_df():
    characters_df = pd.read_csv(os.path.join(CMU_DATASET_PATH, CHARACTER_METADATA), sep='\t', names=characters_label)
    return characters_df


def load_movies_df():
    movies_df = pd.read_csv(os.path.join(CMU_DATASET_PATH, MOVIE_METADATA), sep='\t', names=movies_label)

    movies_df['movie_languages'] = movies_df['movie_languages'].apply(json.loads)
    movies_df['movie_countries'] = movies_df['movie_countries'].apply(json.loads)
    movies_df['movie_genres'] = movies_df['movie_genres'].apply(json.loads)

    return movies_df


def load_plot_df():
    plot_df =  pd.read_csv(os.path.join(CMU_DATASET_PATH, PLOT_SUMMARIES), sep='\t', names=plot_label)
    return plot_df


def load_tvtropes_df():
    tvtropes_df = pd.read_csv(os.path.join(CMU_DATASET_PATH, TVTROPES_CLUSTERS), sep='\t', names=tvtropes_label)
    
    tvtropes_df['character_data'] = tvtropes_df['character_data'].apply(json.loads)
    return tvtropes_df


def load_imdb_ratings():
    imdb_ratings_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_REVIEWS_METADATA), sep='\t')
    return imdb_ratings_df


def load_imdb_basics():
    imdb_names_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_BASICS_METADATA), dtype={4: str}, sep='\t')
    # Only keep the ones labeled as movies
    imdb_names_df = imdb_names_df[imdb_names_df['titleType'] == 'movie']
    return imdb_names_df


def load_imdb_crew():
    imdb_crew_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_CREW_METADATA), sep='\t')
    return imdb_crew_df



def load_imdb_akas():
    imdb_akas_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_AKAS_METADATA), sep='\t')
    return imdb_akas_df



def load_imdb_episodes():
    imdb_episodes_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_EPISODE_METADATA), sep='\t')
    return imdb_episodes_df



def load_imdb_principals():
    imdb_principals_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_PRINCIPAL_METADATA), sep='\t')
    return imdb_principals_df
