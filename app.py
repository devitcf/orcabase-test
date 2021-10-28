import hashlib
import func.auth as auth
import streamlit as st

def init():
    st.set_page_config('Orca base test')
    if 'login' not in st.session_state:
        st.session_state.login = False
    if 'user' not in st.session_state:
    	st.session_state.user = None
    if 'route' not in st.session_state:
        st.session_state.route = 'login'

def login():
    if st.session_state.username and st.session_state.password:
        try:
            user = auth.validate(st.session_state.username, st.session_state.password)
        except Exception as e:
            return st.error(e)
        st.session_state.login = True
        st.session_state.user = user

def register():
    if st.session_state.username and st.session_state.password and st.session_state.name:
        try:
            user = auth.register(st.session_state.username, st.session_state.password, st.session_state.name)
        except Exception as e:
            return st.error(e)
        st.success('Register successful')
        st.session_state.login = True
        st.session_state.user = user
        st.session_state.route = 'dashboard'

def change_pass():
    pass

def logout():
    # Delete all keys from session
    for key in st.session_state.keys():
        del st.session_state[key]
    st.success('Logout successful')

# Init session state
init()
st.session_state

# Sidebar
side_bar = st.sidebar

# Content
content = st.empty()

# Show diff btn if authenticated
with side_bar.container():
    if not (st.session_state.login and st.session_state.user):
        login_route = side_bar.button('Login')
        if login_route:
            st.session_state.route = 'login'
        register_route = side_bar.button('Register')
        if register_route:
            st.session_state.route = 'register'
    else:
        st.header('Welcome, {0}!'.format(st.session_state.user.get('name')))
        change_pass_route = side_bar.button('Change Password')
        if change_pass_route:
            st.session_state.route = 'change_pass'
        side_bar.button('Logout', 'logout_btn', on_click=logout)

# Login form
if not st.session_state.login and st.session_state.route=='login':
    container = content.container()
    container.title('Login')
    with container.form("login_form", True):
        st.text_input('Username', key='username')
        st.text_input('Password', key='password', type='password')
        st.form_submit_button('Login', 'login_btn', on_click=login)

# Register form
if st.session_state.route=='register':
    container = content.container()
    container.title('Register')
    with container.form("register_form", True):
        st.text_input('Username', key='username')
        st.text_input('Password', key='password', type='password')
        st.text_input('Nickname', key='name')
        st.form_submit_button('Register', 'register_btn', on_click=register)

# Dashboard
if st.session_state.route=='dashboard':
    container = content.container()
    container.title('Dashboard')