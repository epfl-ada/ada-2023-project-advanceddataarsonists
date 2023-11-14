import pandas as pd
import os
import json
import numpy as np
import json
from collections import defaultdict
import ast

CMU_DATASET_PATH = "data/cmu/MovieSummaries"
CHARACTER_METADATA = "character.metadata.tsv"
MOVIE_METADATA = "movie.metadata.tsv"
PLOT_SUMMARIES = "plot_summaries.txt"
TVTROPES_CLUSTERS = "tvtropes.clusters.txt"

CMU_PERSONAS_PATH = "data/cmu/personas"
CMU_CHARACTER_PERSONA = "25.100.lda.log.txt"

IMDB_PATH = "data/imdb/"
IMDB_TITLE_RATINGS = "title.ratings.tsv"
IMDB_TITLE_BASICS = "title.basics.tsv"
IMDB_TITLE_PRINCIPALS = "title.principals.tsv"
IMDB_NAME_BASICS = "name.basics.tsv"

TVTROPES_PATH = "data/tvtropes/"
TVTROPES_PERSONAS = "trope2characters.json"

WIKIDATA_PATH = "data/wikidata/"
WIKIDATA_TRANSLATION_ID = "id-translation.wikidata.json"
WIKIDATA_CHARACTERS_TRANSLATION_ID = "id-translation-characters.wikidata.json"

characters_label = ['wiki_movie_id', 'freebase_movie_id', 'release_date', 'character_name', 'actor_birth', 
                    'actor_gender', 'actor_height', 'actor_ethnicity', 'actor_name', 'release_actor_age', 
                    'freebase_map_id', 'freebase_character_id', 'freebase_actor_id']

movies_label = ['wiki_movie_id', 'freebase_movie_id', 'movie_name', 'movie_release_date', 'box_office',
               'movie_runtime', 'movie_languages', 'movie_countries', 'movie_genres']

plot_label = ['wiki_movie_id', 'plot_summary']

tvtropes_label = ['trope_name', 'character_data']

personas_label = ['freebase_id', 'wiki_id', 'movie_name', 'secondary_name', 'full_name', 'token_occurences', 'estimated_trope', 'trope_distrib']


def _load_json_translation_df(path):
    with open(os.path.join(WIKIDATA_PATH, path)) as file:
        raw_table = json.load(file)

    imdb_id = []
    freebase_id = []

    for robject in raw_table['results']['bindings']:
        imdb_id.append(robject['IMDb_ID']['value'])
        freebase_id.append(robject['freebase_id']['value'])

    return pd.DataFrame(data={ 'imdb_id': imdb_id, 'freebase_id': freebase_id })

def load_translation_df():
    """
    Load the dataframe that allow joining between CMU and IMDb movie datasets
    This dataframe contains 2 columns : the freebase ID and the IMDb ID for a given movie

    Returns
    -------
    pandas.DataFrame
        The translation dataframe
    """

    return _load_json_translation_df(WIKIDATA_TRANSLATION_ID)
    


def load_actors_translation_df():
    """
    Load the dataframe that allow joining between CMU and IMDb actors datasets
    This dataframe contains 2 columns : the freebase ID and the IMDb ID for a given actor

    Returns
    -------
    pandas.DataFrame
        The translation dataframe
    """

    return _load_json_translation_df(WIKIDATA_CHARACTERS_TRANSLATION_ID)


def load_characters_df():
    """
    Load the character dataframe of the CMU dataset. Each feature must be separated by a '\t'.

    Returns
    -------
    pandas.DataFrame
        The character dataframe
    """

    characters_df = pd.read_csv(os.path.join(CMU_DATASET_PATH, CHARACTER_METADATA), sep='\t', names=characters_label)
    return characters_df


def load_movies_df():
    """
    Load the movies dataframe of the CMU dataset. Each feature must be separated by a '\t'.
    Note that this function automatically convert column types to dictionary type for the relevant features

    Returns
    -------
    pandas.DataFrame
        The movies dataframe
    """

    movies_df = pd.read_csv(os.path.join(CMU_DATASET_PATH, MOVIE_METADATA), sep='\t', names=movies_label)

    movies_df['movie_languages'] = movies_df['movie_languages'].apply(json.loads)
    movies_df['movie_countries'] = movies_df['movie_countries'].apply(json.loads)
    movies_df['movie_genres'] = movies_df['movie_genres'].apply(json.loads)

    return movies_df


def load_plot_df():
    """
    Load the plot dataframe of the CMU dataset. Each feature must be separated by a '\t'.

    Returns
    -------
    pandas.DataFrame
        The plot dataframe
    """

    plot_df =  pd.read_csv(os.path.join(CMU_DATASET_PATH, PLOT_SUMMARIES), sep='\t', names=plot_label)
    return plot_df


def load_tvtropes_df():
    """
    Load the tvtropes dataframe of the CMU dataset. Each feature must be separated by a '\t'.

    Returns
    -------
    pandas.DataFrame
        The tvtropes dataframe
    """

    tvtropes_df = pd.read_csv(os.path.join(CMU_DATASET_PATH, TVTROPES_CLUSTERS), sep='\t', names=tvtropes_label)
    
    tvtropes_df['character_data'] = tvtropes_df['character_data'].apply(json.loads)
    return tvtropes_df


def load_imdb_ratings():
    """
    Load the IMDb ratings dataframe. Each feature must be separated by a '\t'.

    Returns
    -------
    pandas.DataFrame
        The IMDb ratings dataframe
    """

    imdb_ratings_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_TITLE_RATINGS), sep='\t')
    return imdb_ratings_df


def load_imdb_title_basics():
    """
    Load the IMDb title basics dataframe describing the basic features of a movie title.
    Note that we only load the IMDb titles labeled as "movie"
    Each feature must be separated by a '\t'.

    Returns
    -------
    pandas.DataFrame
        The IMDb title basics dataframe
    """

    imdb_names_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_TITLE_BASICS), dtype={4: str}, sep='\t')
    # Only keep the ones labeled as movies
    imdb_names_df = imdb_names_df[imdb_names_df['titleType'] == 'movie']

    imdb_names_df["genres"] = imdb_names_df["genres"].apply(lambda s : s.split(",") if s != '\\N' else s)

    return imdb_names_df


def load_imdb_title_principals():
    """
    Load the IMDb title principals dataframe describing the detailed features of a movie title.
    Each feature must be separated by a '\t'.

    Returns
    -------
    pandas.DataFrame
        The IMDb title principals dataframe
    """

    imdb_principals_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_TITLE_PRINCIPALS), sep='\t')
    return imdb_principals_df


def load_imdb_person_basics():
    """
    Load the IMDb name basics dataframe describing the basic features of a person.
    Each feature must be separated by a '\t'.

    Returns
    -------
    pandas.DataFrame
        The IMDb person basics dataframe
    """

    imdb_name_basics_df = pd.read_csv(os.path.join(IMDB_PATH, IMDB_NAME_BASICS), sep='\t')

    imdb_name_basics_df["primaryProfession"] = imdb_name_basics_df["primaryProfession"].apply(lambda s : s.split(",") if pd.notnull(s) else s)
    imdb_name_basics_df["knownForTitles"] = imdb_name_basics_df["knownForTitles"].apply(lambda s : s.split(",") if pd.notnull(s) else s)

    return imdb_name_basics_df


def load_personas():
    """
    Load personas generated by the CMU pipeline.
    
    Returns
    -------
    pandas.DataFrame
        The personas dataframe generated by the CMU pipeline
    """

    personas_df = pd.read_csv(os.path.join(CMU_PERSONAS_PATH, CMU_CHARACTER_PERSONA), sep='\t', names=personas_label)
    personas_df['trope_distrib'] = personas_df['trope_distrib'].apply(lambda x : np.fromstring(x, dtype=np.float32, sep=' '))
    return personas_df


def load_tv_tropes_personas_df():
    """
    Load personas loaded from the tvtropes website.

    Returns
    -------
    pandas.DataFrame
        The personas dataframe according to tvtopes website
    """

    tv_tropes_personas_path = os.path.join(TVTROPES_PATH, TVTROPES_PERSONAS)
    
    with open(tv_tropes_personas_path, 'r') as file:
        trope2characters_data = json.load(file)
        
    movie_ids = []
    for trope, characters in trope2characters_data.items():
        for char_info in characters:
            char_dict = ast.literal_eval(char_info.strip())
            movie_id = char_dict["id"]
            actor = char_dict["actor"]
            movie = char_dict["movie"]
            character = char_dict["char"]
            movie_ids.append({"id": movie_id, "trope": trope, "actor": actor, "character": character, "movie_name": movie})
    return pd.DataFrame(movie_ids)