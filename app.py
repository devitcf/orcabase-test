import hashlib
import func.auth as auth
import streamlit as st

def init():
    if 'login' not in st.session_state:
        st.session_state.login = False
    if 'user' not in st.session_state:
    	st.session_state.user = None

def login():
    if st.session_state.username and st.session_state.password:
        try:
            user = auth.validate(st.session_state.username, st.session_state.password)
        except Exception as e:
            return st.error(e)
        st.session_state.login = True
        st.session_state.user = user

def logout():
    # Delete all keys from session
    for key in st.session_state.keys():
        del st.session_state[key]
    st.success('Logout successful')

# Init session state
init()

# Main title
st.title('Orca base Test')

# Login form
if not st.session_state.login:
    with st.form("login_form", True):
        st.header('Login')
        st.text_input('Username', key='username')
        st.text_input('Password', key='password', type='password')
        st.form_submit_button('Login', 'Login', on_click=login)

# Sidebar
if st.session_state.login and st.session_state.user:
    with st.sidebar.container():
        st.header('Welcome, {0}!'.format(st.session_state.user.get('name')))
        st.sidebar.button('Logout', 'Logout', on_click=logout)