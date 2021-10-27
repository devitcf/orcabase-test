import hashlib
import func.auth as auth
import streamlit as st

# Init session state
if 'login' not in st.session_state:
    st.session_state.login = False
if 'user' not in st.session_state:
	st.session_state.user = None

def login():
    user = auth.validate(st.session_state.username, st.session_state.password)
    if user is None:
        return st.error("Incorrect username or password")
    else:
        st.session_state.login = True
        st.session_state.user = user

def logout():
    # Delete all keys from session
    for key in st.session_state.keys():
        del st.session_state[key]
    st.success('Logout successful')

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
if st.session_state.login:
    with st.sidebar.container():
        st.header('Welcome, {0}!'.format(st.session_state.user.get('name')))
        st.sidebar.button('Logout', 'Logout', on_click=logout)