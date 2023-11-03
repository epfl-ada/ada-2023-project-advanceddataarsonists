import requests
from tqdm import tqdm
from os.path import join, exists, basename, split
from os import makedirs
import shutil
from urllib.parse import urlparse

DATASET_PATH = join('.', 'dataset')
DATASET_CACHE_PATH = join('.', 'dataset', 'cache')

def unpack_gz(gzipped_file_name, work_dir):
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

def ensure_database_availability():
    # Dataset to download
    datasets = [
        'https://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz',
        'https://datasets.imdbws.com/title.basics.tsv.gz',
        'https://datasets.imdbws.com/name.basics.tsv.gz',
        'https://datasets.imdbws.com/title.ratings.tsv.gz',
        'https://datasets.imdbws.com/title.principals.tsv.gz'
    ]

    # Download each dataset one by one
    makedirs(DATASET_PATH, exist_ok=True)
    makedirs(DATASET_CACHE_PATH, exist_ok=True)

    for dataset in datasets:
        filename = basename(urlparse(dataset).path)
        archive_path = join(DATASET_CACHE_PATH, filename)

        if exists(archive_path):
            print(f'[+] Found cached dataset for url {dataset}')
        
        else:
            print(f'[x] No cached data for url {dataset}')
            download(dataset, archive_path)

            print(f'  - Extracting archive {dataset}')
            shutil.unpack_archive(archive_path, DATASET_PATH)
    
if __name__ == '__main__':
    ensure_database_availability()