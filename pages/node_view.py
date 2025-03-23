import streamlit as st
import os
from tools.queries import get_topic_lesson

# Check if topic and node is in session_state if not redirect to landing or graph_view
if ('topic' not in st.session_state) or ('node' not in st.session_state) or (st.session_state['node'] is None):
    st.write("Please switch to the landing page to select a topic or graph view to select a topic and a node!")

    # Redirect buttons 
    st.button("Go to Landing", key="landing")
    st.button("Go to Graph View", key="graph_view")

    if st.session_state['landing']:
        st.session_state['page'] = "Landing"
        st.switch_page("pages/landing.py")
    elif st.session_state['graph_view']:
        st.session_state['page'] = "Graph View"
        st.switch_page("pages/graph_view.py")
else:
    # Check if the node file exists
    if not st.session_state['node'].endswith(".md"):
        st.session_state['node'] = f"{st.session_state['node']}.md"
    if not (os.path.exists(f"./data/{st.session_state['topic']}/{st.session_state['node']}")):
        topic_prompter = st.session_state['topic']
        node_prompter = st.session_state['node'].replace(".md", "")
        node_parent_prompter = st.session_state['node_parent'].replace(".md", "")
        topic_data = get_topic_lesson(topic_prompter, node_prompter, node_parent_prompter)
        with open(f"./data/{st.session_state['topic']}/{st.session_state['node']}", "w", encoding="utf-8") as f:
            f.write(topic_data)
    # Display the node file
    with open (f"./data/{st.session_state['topic']}/{st.session_state['node']}", 'r') as f:
        st.title(st.session_state['node'].replace(".md", ""))
        st.write(f.read())
