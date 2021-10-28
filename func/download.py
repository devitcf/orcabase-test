import urllib
import datetime

def download(from_date, to_date):
    print(from_date.year)
    url = 'https://api.data.gov.hk/v1/historical-archieve/get-file?url={0}&time={1}'.format(urllib.parse.quote_plus('https://resource.data.one.gov.hk/td/speedmap.xml'), from_date)
    print(url)