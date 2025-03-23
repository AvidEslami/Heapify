import streamlit as st
import os

st.title("Welcome to the Decompissect Fragsolveductitionanalysegment Factor!")
st.write("This is a tool to help you understand the WORLD>~!.")

st.text_input("Enter a topic to learn about:", placeholder="examples: [Dark Philosophy, CNN's, Pokemon, Web Dev, Naruto's Mom]", key="input")

st.button("Start Exploring", key="start")

# Check for folders in ./data and display them as options
options = []
for folder in os.listdir("./data"):
    if os.path.isdir(f"./data/{folder}"):
        options.append(folder)
st.selectbox("Or continue learning about one of the previously selected topics:", options, placeholder='', index=None, key="previous")
# On button press, save the topic to session_state and redirect to graph_view
if st.session_state['start'] and st.session_state['start'] != "examples: [Dark Philosophy, CNN's, Pokemon, Web Dev, Naruto's Mom]":
    topic = st.session_state['input']

    # Clear the session state
    for key in st.session_state.keys():
        del st.session_state[key]

    st.session_state['topic'] = topic
    st.session_state['page'] = "Graph View"
    st.session_state['node'] = None
    st.switch_page("pages/graph_view.py")

elif st.session_state['previous']:
    topic = st.session_state['previous']

    # Clear the session state
    for key in st.session_state.keys():
        del st.session_state[key]

    st.session_state['topic'] = topic
    st.session_state['page'] = "Graph View"
    st.session_state['node'] = None
    st.switch_page("pages/graph_view.py")