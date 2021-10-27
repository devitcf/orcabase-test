import os
import hashlib
import func.connection as conn
import pymongo
import streamlit as st

def validate(username, password):
    # Return none if empty
    if not (username and password):
        return None

    # Get MongoDB connection
    db = conn.get_db()
    if db is None:
        return st.error("Couldn't connect to Database")

    # Return user if validate success
    user = db.users.find_one({"username": username})
    if not (user and (user['password'] == hashlib.pbkdf2_hmac('sha256', st.session_state.password.encode('utf-8'), user['salt'], 100000))):
        return None
    else:
        return user

# def register(name, username, password):
#     # Get MongoDB connection
#     db = conn.get_db()
#     if db is None:
#         return st.error("Couldn't connect to Database")
#
#     salt = os.urandom(32)
#     user = {
#         "name": name,
#         "username": username,
#         "salt": salt,
#         "password": hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
#     }
#     try:
#         return db.users.insert_one(user).inserted_id
#     except:
#         return st.error('Register fail')