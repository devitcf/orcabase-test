import urllib
import datetime
import requests

def download(from_date, to_date):
    # Define api url and exception
    traffic_api = 'https://resource.data.one.gov.hk/td/speedmap.xml'
    list_file_version_api = 'https://api.data.gov.hk/v1/historical-archive/list-file-versions'
    get_file_api = 'https://api.data.gov.hk/v1/historical-archive/get-file'
    error = Exception('Fetch traffic date fail')

    # Get all the file version for the period of time
    params = {'url': traffic_api, 'start': from_date.strftime('%Y%m%d'), 'end': to_date.strftime('%Y%m%d')}
    result = requests.get(list_file_version_api, params=params)
    print(params)
    print(result.url)

    # Raise exception if response code is not 200
    if result.status_code is not 200:
        raise error

    timestamps = result.json().get('timestamps')
    timestamp = timestamps[0]
    result = requests.get(get_file_api, params={'url': params.get('url'), 'time': timestamp})
    print(result.text)
#     for timestamp in result.json().get('timestamps'):
#         params = {'url': traffic_api, }
#         print()