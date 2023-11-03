import pandas as pd
import os
import json

DATASET_PATH = "dataset/"
CHARACTER_METADATA = "character.metadata.tsv"
MOVIE_METADATA = "movie.metadata.tsv"
PLOT_SUMMARIES = "plot_summaries.txt"
TVTROPES_CLUSTERS = "tvtropes.clusters.txt"


characters_label = ['wiki_movie_id', 'freebase_movie_id', 'release_date', 'character_name', 'actor_birth', 
                    'actor_gender', 'actor_height', 'actor_ethnicity', 'actor_name', 'release_actor_age', 
                    'freebase_map_id', 'freebase_character_id', 'freebase_actor_id']

movies_label = ['wiki_movie_id', 'freebase_movie_id', 'movie_name', 'movie_release_date', 'box_office',
               'movie_runtime', 'movie_languages', 'movie_countries', 'movie_genres']

plot_label = ['wiki_movie_id', 'plot_summary']

tvtropes_label = ['trope_name', 'character_data']

def load_characters_df():
    characters_df = pd.read_csv(os.path.join(DATASET_PATH, CHARACTER_METADATA), sep='\t', names=characters_label)
    return characters_df


def load_movies_df():
    movies_df = pd.read_csv(os.path.join(DATASET_PATH, MOVIE_METADATA), sep='\t', names=movies_label)

    movies_df['movie_languages'] = movies_df['movie_languages'].apply(json.loads)
    movies_df['movie_countries'] = movies_df['movie_countries'].apply(json.loads)
    movies_df['movie_genres'] = movies_df['movie_genres'].apply(json.loads)

    return movies_df


def load_plot_df():
    plot_df =  pd.read_csv(os.path.join(DATASET_PATH, PLOT_SUMMARIES), sep='\t', names=plot_label)
    return plot_df


def load_tvtropes_df():
    tvtropes_df = pd.read_csv(os.path.join(DATASET_PATH, TVTROPES_CLUSTERS), sep='\t', names=tvtropes_label)
    
    tvtropes_df['character_data'] = tvtropes_df['character_data'].apply(json.loads)
    return tvtropes_df


