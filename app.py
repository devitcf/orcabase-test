import streamlit as st
import pymongo

# Initialize mongodb connection
client = pymongo.MongoClient("mongodb+srv://{0}:{1}@cluster0.igs5e.mongodb.net/?retryWrites=true&w=majority".format(st.secrets['mongo']['username'], st.secrets['mongo']['password']))
db = client[st.secrets['mongo']['dbname']]

st.title('Login')
# Pull data from the collection
# Uses st.cache to only rerun when the query changes or after 10 min
@st.cache(ttl=600)
def get_users():
    db = client.orcabase
    items = db.users.find()
    items = list(items)  # make hashable for st.cache
    return items

items = get_users()

items