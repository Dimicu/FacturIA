import  streamlit as st

class logout():
    def logoutbutton(self):
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['email'] = ""
            st.session_state.authenticated = False
            st.rerun()