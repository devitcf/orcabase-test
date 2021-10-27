import pymongo
import streamlit as st

def get_db():
    # Initialize MongoDB connection
    try:
        client = pymongo.MongoClient("mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority".format(st.secrets['mongo']['username'], st.secrets['mongo']['password'], st.secrets['mongo']['host']))
        return client[st.secrets['mongo']['database']]
    except:
        return None