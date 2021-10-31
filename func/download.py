import os
import urllib
import datetime
import requests
import streamlit as st
import threading

# Define api url and exception
traffic_api = 'https://resource.data.one.gov.hk/td/speedmap.xml'
list_file_version_api = 'https://api.data.gov.hk/v1/historical-archive/list-file-versions'
get_file_api = 'https://api.data.gov.hk/v1/historical-archive/get-file'
error = Exception('Fetch traffic date fail')

def download(from_date, to_date):
    global traffic_api, list_file_version_api, get_file_api, error, count
    # Get all the file version for the period of time
    params = {'url': traffic_api, 'start': from_date.strftime('%Y%m%d'), 'end': to_date.strftime('%Y%m%d')}
    result = requests.get(list_file_version_api, params=params)
    print(result.url)

    # Raise exception if response code is not 200
    if result.status_code != 200:
        raise error

    timestamps = result.json().get('timestamps')
    total = result.json().get('version-count')

    # Create folder if not exist
    if not os.path.exists('data'):
        os.mkdir('data')

    # Define thread list
    thread_list = []
    for timestamp in timestamps:
        thread_list.append(threading.Thread(target=download_xml, args=[timestamp]))

    # Prepare a spinner and start the thread
    with st.spinner('Preparing data...'):
        for t in thread_list:
            print(t.start())

    # Return when all the threads done
    return t.join()


def download_xml(timestamp):
    global traffic_api, get_file_api, error
    path = 'data/{0}.xml'.format(timestamp)

    # if file already exists, do not download
    if not os.path.exists(path):
        response = requests.get(get_file_api, params={'url': traffic_api, 'time': timestamp})
        if response.status_code != 200:
            raise Exception(error)
        with open(path, 'wb') as file:
            file.write(response.content)