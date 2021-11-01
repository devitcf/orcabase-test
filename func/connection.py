import pymongo
import s3fs
import streamlit as st

def get_db():
    # Initialize MongoDB connection
    try:
        client = pymongo.MongoClient("mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority".format(st.secrets['mongo']['username'], st.secrets['mongo']['password'], st.secrets['mongo']['host']))
        return client[st.secrets['mongo']['database']]
    except:
        return None

def get_aws_s3():
    # Initialize AWS S3 connection
    try:
        return s3fs.S3FileSystem(False, st.secrets['aws_s3']['access_key_id'], st.secrets['aws_s3']['secret_access_key'])
    except:
        return None
