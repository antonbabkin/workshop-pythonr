"""Data preparation module."""

print('scripts.data module is being imported')


from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict

import requests
import pandas
import geopandas


def download_file(url, dir=None, fname=None, overwrite=False):
    """Download file from given `url` and put it into `dir`.
    Current working directory is used as default. Missing directories are created.
    File name from `url` is used as default, but can be replaced with `fname`.
    Return absolute pathlib.Path of the downloaded file.
    """
    
    if dir is None:
        dir = '.'
    dpath = Path(dir).resolve()
    if not dpath.exists():
        print(f'Creating directory {dpath}')
        dpath.mkdir(parents=True)

    if fname is None:
        fname = Path(urlparse(url).path).name
    fpath = dpath / fname
    
    if not overwrite and fpath.exists():
        print(f'File already exists at {fpath}')
        return fpath

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fpath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=2**20):
                f.write(chunk)
    
    print(f'Downloaded file to {fpath}')
    return fpath


def get_bds_df(geo):
    """Return dataframe with Business Dynamics Statistics.
    `geo` sets unit of observation and can be "nation", "state" or "county".
    Automatically downloads raw file.
    """

    cache_path = Path(f'data/bds_{geo}.parquet')
    if cache_path.exists():
        print(f'Read from cache {cache_path}')
        return pandas.read_parquet(cache_path)

    if geo == 'nation':
        url = 'https://www2.census.gov/programs-surveys/bds/tables/time-series/2021/bds2021.csv'
    elif geo == 'state':
        url = 'https://www2.census.gov/programs-surveys/bds/tables/time-series/2021/bds2021_st.csv'
    elif geo == 'county':
        url = 'https://www2.census.gov/programs-surveys/bds/tables/time-series/2021/bds2021_st_cty.csv'

    dtypes = defaultdict(
        lambda: 'Int32',
        year='int16',
        estabs_entry_rate='Float32',
        estabs_exit_rate='Float32',
        job_creation_rate_births='Float32',
        job_creation_rate='Float32',
        job_destruction_rate_deaths='Float32',
        job_destruction_rate='Float32',
        net_job_creation_rate='Float32',
        reallocation_rate='Float32'
    )
    if geo in ['state', 'county']:
        dtypes['st'] = 'str'
    if geo == 'county':
        dtypes['cty'] = 'str'

    raw_path = download_file(url, dir='data/raw')

    df = pandas.read_csv(raw_path, dtype=dtypes, na_values=['S', 'D', 'N'])

    if geo == 'county':
        df['fips'] = df['st'] + df['cty']

    print(f'Save to cache {cache_path}')
    df.to_parquet(cache_path)

    return df


def get_ui_df():
    """Return dataframe with US counties classified by the 2013 revision of ERS Urban Influence Codes.
    Automatically downloads raw file.
    """

    cache_path = Path('data/uic.parquet')
    if cache_path.exists():
        print(f'Read from cache {cache_path}')
        return pandas.read_parquet(cache_path)
    
    url = 'https://www.ers.usda.gov/webdocs/DataFiles/53797/UrbanInfluenceCodes2013.xls?v=4919.6'
    raw_path = download_file(url, dir='data/raw', fname='UrbanInfluenceCodes2013.xls')
    
    df = pandas.read_excel(raw_path, dtype=str)\
        .rename(columns=str.lower)\
        .rename(columns={'state': 'state_abbr', 'population_2010': 'population', 'uic_2013': 'uic', 'description': 'uic_desc'})
    df['population'] = df['population'].astype('int32')
    df['uic'] = df['uic'].astype('int8')

    print(f'Save to cache {cache_path}')
    df.to_parquet(cache_path)

    return df


def get_county_shape_df():
    """Return geodataframe of county shapes.
    Automatically downloads raw file.
    """
    cache_path = Path('data/county_shp.parquet')
    if cache_path.exists():
        print(f'Read from cache {cache_path}')
        return geopandas.read_parquet(cache_path)
    
    # url = 'https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_20m.zip'
    url = 'https://www2.census.gov/geo/tiger/GENZ2013/cb_2013_us_county_20m.zip'
    raw_path = download_file(url, dir='data/raw')
    df = geopandas.read_file(raw_path).rename(columns=str.lower)
    df['fips'] = df['geoid']

    print(f'Save to cache {cache_path}')
    df.to_parquet(cache_path)
    
    return df