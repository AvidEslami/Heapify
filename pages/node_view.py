import streamlit as st

with open (f"./data/{st.session_state['node']}", 'r') as f:
    st.write(f.read())