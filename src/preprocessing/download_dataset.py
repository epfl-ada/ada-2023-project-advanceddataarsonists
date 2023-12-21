import requests
import shutil
import json
from tqdm import tqdm
from os.path import join, exists, basename, split
from os import makedirs, walk, remove
from urllib.parse import urlparse
import textwrap

DATASET_PATH = join('.', 'data')
DATASET_CACHE_PATH = join('.', 'data', 'cache')
WIKIDATA_QUERY_URL = 'https://query.wikidata.org/sparql'

def unpack_gz(gzipped_file_name, work_dir):
    """
    Unzip file or folder using 'gz'. The unzipped file is 'work_dir/gzipped_file_name' 
    and is unzipped in the same work_dir

    Parameters
    ----------
    gzipped_file_name : str
        File name
    work_dir : str
        Working directory    
    """

    filename = split(gzipped_file_name)[-1]
    filename = re.sub(r"\.gz$", "", filename, flags=re.IGNORECASE)

    with gzip.open(gzipped_file_name, 'rb') as f_in:
        with open(join(work_dir, filename), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

try:
    import gzip, re
    shutil.register_unpack_format('gz', ['.gz',], unpack_gz)
except Exception as e:
    print('[x] Fail to register archieve format .gz (make sure requirements.txt are satisfied)')
    print(e)


def download(url: str, fname: str, chunk_size=1024):
    """
    Download file at url and stores it in a file named fname
    
    Parameters
    ----------
    url : str
        URL pointing to the file
    fname : str
        Name of the file to store the data
    chunk_size : int, optional
        Size of the chunk used to iterate the GET response from the URL (default is 1024)
    """

    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))

    with open(fname, 'wb') as file, tqdm(
        desc=f'  - Downloading {fname}',
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=chunk_size
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)


def download_wikidata_query(query: str, file: str):
    """
    Send a query to the WikiData database.
    This function queries the WIKIDATA_QUERY_URL website.

    Parameters
    ----------
    query : str
        The query to send
    file : str
        The name of the file to store the result of the query
    """

    print('  - Running query: "{}" (this may take a while)'.format(textwrap.shorten(query.replace('\n', ' '), width=16)))
    r = requests.get(url=WIKIDATA_QUERY_URL, params={ 'format': 'json', 'query': query })
    obj = r.json()

    print('  - Serialization of the result')
    with open(file, 'w') as file:
        json.dump(obj, file)

def ensure_database_availability():
    """
    Download the datasets needed for the analysis.
    This will create the missing directories if any
    """

    # Dataset to download
    datasets = [
        ('https://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz', 'cmu'),
        # ('https://www.cs.cmu.edu/~ark/personas/data/corenlp_plot_summaries.tar', 'cmu'),
        ('https://datasets.imdbws.com/title.basics.tsv.gz', 'imdb'),
        ('https://datasets.imdbws.com/name.basics.tsv.gz', 'imdb'),
        ('https://datasets.imdbws.com/title.ratings.tsv.gz', 'imdb'),
        ('https://datasets.imdbws.com/title.principals.tsv.gz', 'imdb'),        
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/25.100.lda.cond.log.txt.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/25.100.lda.log.txt.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/featureFile.txt.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/featureMeans.txt.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/lr.weights.txt.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/out.phi.weights.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/personaFile.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/finalLAgentsFile.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/finalLModFile.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/personas/finalLPatientsFile.gz", "cmu/personas"),
        ("https://raw.githubusercontent.com/MichelDucartier/ACL_personas_dump/master/tvtropes/trope2characters.json.gz", "tvtropes")
    ]

    # Download each dataset one by one
    makedirs(DATASET_PATH, exist_ok=True)
    makedirs(DATASET_CACHE_PATH, exist_ok=True)

    for dataset, folder in datasets:
        working_dir = join(DATASET_PATH, folder)
        makedirs(working_dir, exist_ok=True)
        
        filename = basename(urlparse(dataset).path)
        archive_path = join(DATASET_CACHE_PATH, filename)

        if exists(archive_path):
            print(f'[+] Found cached dataset for url {dataset}')
        
        else:
            print(f'[x] No cached data for url {dataset}')
            download(dataset, archive_path)

            print(f'  - Extracting archive {dataset}')
            shutil.unpack_archive(archive_path, working_dir)


    translation_id_wikidata_path = join(DATASET_PATH, 'wikidata')
    makedirs(translation_id_wikidata_path, exist_ok=True)
    translation_id_wikidata_path = join(translation_id_wikidata_path, 'id-translation.wikidata.json')

    if exists(translation_id_wikidata_path):
        print('[+] Found existing translation for wiki_movie_id to imdb\' tconst')
    
    else:
        query = '''
        SELECT DISTINCT ?item ?IMDb_ID ?freebase_id ?title WHERE {
            ?item p:P31/ps:P31/wdt:P279* wd:Q11424 .
            ?item wdt:P345 ?IMDb_ID .
            ?item wdt:P646 ?freebase_id .
            ?item wdt:P1476 ?title .
            ?item wdt:P577 ?pub_date
            FILTER(YEAR(?pub_date) <= 2012).
        }
        '''

        print('[x] No cached data for translation for wiki_movie_id to imdb\' tconst')
        result = download_wikidata_query(query=query, file=translation_id_wikidata_path)

    translation_characters_id_wikidata_path = join(DATASET_PATH, 'wikidata')
    translation_characters_id_wikidata_path = join(translation_characters_id_wikidata_path, 'id-translation-characters.wikidata.json')

    if exists(translation_characters_id_wikidata_path):
        print('[+] Found existing translation for characters wiki id to imdb\' tconst')
    
    else:
        query = '''
        SELECT DISTINCT ?actor ?IMDb_ID ?freebase_id
        WHERE {
            ?actor wdt:P106 wd:Q33999 .
            ?actor wdt:P345 ?IMDb_ID .
            ?actor wdt:P646 ?freebase_id .
        }
        '''

        print('[x] No cached data for translation for characters wiki id to imdb\' tconst')
        result = download_wikidata_query(query=query, file=translation_characters_id_wikidata_path)
        

if __name__ == '__main__':
    ensure_database_availability()