import os
import urllib
import datetime
import requests
import streamlit as st
import dask.bag as db
import dask.dataframe as dd
from dask.delayed import delayed

# Define api url and exception
traffic_api = 'https://resource.data.one.gov.hk/td/speedmap.xml'
list_file_version_api = 'https://api.data.gov.hk/v1/historical-archive/list-file-versions'
get_file_api = 'https://api.data.gov.hk/v1/historical-archive/get-file'
error = Exception('Fetch traffic date fail')

def download(from_date, to_date):
    global traffic_api, list_file_version_api, get_file_api, error
    # Get all the file version for the period of time
    params = {'url': traffic_api, 'start': from_date.strftime('%Y%m%d'), 'end': to_date.strftime('%Y%m%d')}
    result = requests.get(list_file_version_api, params=params)
    print(params)
    print(result.url)

    # Raise exception if response code is not 200
    if result.status_code != 200:
        raise error

    timestamps = result.json().get('timestamps')

    if not os.path.exists('data'):
        os.mkdir('data')

    delayed = [delayed(download_xml)(timestamp) for timestamp in timestamps]

    b = db.from_delayed(delayed)
#     df = dd.from_delayed(dfs)
    print(b)

#     dfs = df.to_delayed()
#     for timestamp in timestamps:
#         dask.delayed(download_traffic_data_by_timestamp)(timestamp)
#         expander.write('https://api.data.gov.hk/v1/historical-archive/get-file?url={0}&time={1}'.format(urllib.parse.quote_plus('https://resource.data.one.gov.hk/td/speedmap.xml'), timestamp))

def download_xml(timestamp):
    global traffic_api, list_file_version_api, get_file_api, error
    response = requests.get(get_file_api, params={'url': traffic_api, 'time': timestamp}, stream=True)
    with open('data/{0}.xml'.format(timestamp), 'wb') as file:
        file.write(response.content)
        st.write('Downloading {0}.xml'.format(timestamp))