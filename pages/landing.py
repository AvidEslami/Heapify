import streamlit as st

st.title("Welcome to the Decompissect Fragsolveductitionanalysegment Factor!")
st.write("This is a tool to help you understand the WORLD>~!.")

st.text_input("Enter a topic to learn about:", "Dark Philosophy", key="input")

st.button("Start Exploring", key="start")
# On button press, save the topic to session_state and redirect to graph_view
if st.session_state['start']:
    topic = st.session_state['input']

    # Clear the session state
    for key in st.session_state.keys():
        del st.session_state[key]

    st.session_state['topic'] = topic
    st.session_state['page'] = "Graph View"
    st.session_state['node'] = None
    st.switch_page("pages/graph_view.py")