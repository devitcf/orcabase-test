import hashlib
import datetime
import func.auth as auth
import func.download as dl
import streamlit as st

def init():
    # Set title
    st.set_page_config('Orca base test')
    # Set states for login and routing
    if 'login' not in st.session_state:
        st.session_state.login = False
    if 'user' not in st.session_state:
    	st.session_state.user = None
    if 'route' not in st.session_state:
        st.session_state.route = 'login'

def router(path):
    st.session_state.route=path

def login():
    if st.session_state.username and st.session_state.password:
        try:
            user = auth.validate(st.session_state.username, st.session_state.password)
        except Exception as e:
            return st.error(e)
        st.session_state.login = True
        st.session_state.user = user
        return router('dashboard')

def register():
    if st.session_state.username and st.session_state.password and st.session_state.name:
        try:
            user = auth.register(st.session_state.username, st.session_state.password, st.session_state.name)
        except Exception as e:
            return st.error(e)
        st.session_state.login = True
        st.session_state.user = user
        return router('dashboard')

def change_pass():
    if st.session_state.password:
        try:
            result = auth.change_password(st.session_state.user.get('_id'), st.session_state.password)
        except Exception as e:
            return st.error(e)
        st.success('Change password successful')

def logout():
    # Delete all keys from session
    for key in st.session_state.keys():
        del st.session_state[key]

def download():
    if st.session_state.from_date and st.session_state.to_date:
        if st.session_state.to_date < st.session_state.from_date:
            return st.error('Please input the correct dates')
        try:
            dl.download(st.session_state.from_date, st.session_state.to_date)
        except Exception as e:
            return st.error(e)
        st.success('Completed!')

if __name__ == '__main__':
    # Init session state
    init()

    # Sidebar
    side_bar = st.sidebar

    # Content
    content = st.empty()

    # Show diff btn if authenticated
    with side_bar.container():
        if not (st.session_state.login and st.session_state.user):
            side_bar.button('Login', on_click=router, args=['login'])
            register_route = side_bar.button('Register', on_click=router, args=['register'])
        else:
            st.header('Welcome, {0}!'.format(st.session_state.user.get('name')))
            side_bar.button('Dashboard', on_click=router, args=['dashboard'])
            change_pass_route = side_bar.button('Change Password', on_click=router, args=['change_pass'])
            side_bar.button('Logout', on_click=logout)

    # Login form
    if not st.session_state.login:
        container = content.container()
        container.title('Login')
        with container.form('login_form', True):
            st.text_input('Username', key='username')
            st.text_input('Password', key='password', type='password')
            st.form_submit_button('Login', on_click=login)

    # Register form
    if st.session_state.route=='register':
        container = content.container()
        container.title('Register')
        with container.form('register_form', True):
            st.text_input('Username', key='username')
            st.text_input('Password', key='password', type='password')
            st.text_input('Nickname', key='name')
            st.form_submit_button('Register', on_click=register)

    # Change password form
    if st.session_state.route=='change_pass':
        container = content.container()
        container.title('Change password')
        with container.form('change_pass_form', True):
            st.text_input('Password', key='password', type='password')
            st.form_submit_button('Change', on_click=change_pass)

    # Dashboard
    if st.session_state.route=='dashboard':
        container = content.container()
        container.title('Download traffic data')
        from_date = datetime.date(2021, 8, 1)
        to_date = datetime.date(2021, 10, 1)
        with container.form('download_form'):
            st.date_input('From', key='from_date', value=from_date, min_value=from_date, max_value=to_date)
            st.date_input('To', key='to_date', value=from_date, min_value=from_date, max_value=to_date)
            st.form_submit_button('Download', on_click=download)