import os
import hashlib
import func.connection as conn
import pymongo
import streamlit as st

def validate(username, password):
    # Get MongoDB connection
    db = conn.get_db()
    if db is None:
        raise Exception('Could not connect to database')

    # Return user if validate success
    user = db.users.find_one({"username": username})
    if not (user and (user['password'] == hashlib.pbkdf2_hmac('sha256', st.session_state.password.encode('utf-8'), user['salt'], 100000))):
        raise Exception('Incorrect username or password')
    else:
        return user

def get_salted_password(password):
    # Prepare salt and hashed password
    salt = os.urandom(32)
    return [salt, hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)]

def register(username, password, name):
    # Get MongoDB connection
    db = conn.get_db()
    if db is None:
        raise Exception('Could not connect to database')

    # Check duplicate username
    if db.users.find_one({"username": username}):
        raise Exception('Username already exists')

    # Prepare user data
    salt, salted_pass = get_salted_password(password)
    user = {
        "name": name,
        "username": username,
        "salt": salt,
        "password": salted_pass
    }

    # Try insert to database
    try:
        inserted_id = db.users.insert_one(user).inserted_id
        return db.users.find_one({'_id': inserted_id})
    except:
        raise Exception('Register fail')


def change_password(uid, password):
    # Get MongoDB connection
    db = conn.get_db()
    if db is None:
        raise Exception('Could not connect to database')

    # Prepare user data
    salt, salted_pass = get_salted_password(password)

    # Try update to database
    try:
        return db.users.update_one({'_id': uid}, {'$set': {'salt': salt, 'password': salted_pass} })
    except:
        raise Exception('Register fail')