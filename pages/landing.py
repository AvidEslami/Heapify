import streamlit as st
import os
import shutil

st.set_page_config(layout="wide")

st.title("Welcome to the Decompissect Fragsolveductitionanalysegment Factor!")

st.subheader("Learn Something New!")
st.text_input("Enter a topic to learn about:", placeholder="examples: [Dark Philosophy, CNN's, Pokemon, Web Dev, Naruto's Mom]", key="input")

st.button("Start Exploring", key="start_button")

# Check for folders in ./data and display them as options
options = []
for folder in os.listdir("./data"):
    if os.path.isdir(f"./data/{folder}"):
        options.append(folder)
st.subheader("Continue where you left off")
st.selectbox("Enter one of the previously selected topics:", options, placeholder='', index=None, key="previous")


st.subheader("Delete a topic")
st.selectbox("Enter a previously explored topic to delete it:", options, placeholder='', index=None, key="delete_topic")
# On button press, save the topic to session_state and redirect to graph_view
if st.session_state['input'] and st.session_state['start_button']:
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

elif st.session_state['delete_topic']:
    topic = st.session_state['delete_topic']
    # Make a delete button just to be sure the user wants to delete the topic
    if st.button("🗑️", help="Delete this topic"):
        if os.path.exists(f"./data/{topic}/"):
            shutil.rmtree(f"./data/{topic}")
        st.write(f"Deleted {topic}")
        st.rerun()