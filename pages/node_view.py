import streamlit as st
import os
from tools.queries import get_topic_lesson
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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
    try:
        with open (f"./data/{st.session_state['topic']}/{st.session_state['node']}", 'r') as f:
            # two invisible columns, one with title and the other with a delete node button
            col1, col2, col3 = st.columns([13, 3, 1])  # Wider left column for title, narrower right for button

            with col1:
                st.title(st.session_state['node'].replace(".md", ""))

            with col2: 
                if st.button("Return to Graph View", help="⬅", use_container_width=True):
                    st.switch_page("pages/graph_view.py")
            with col3:
                if st.button("🗑️", help="Delete this node"):
                    st.success("Node deleted.")
                    st.session_state["path_to_delete"] = f"./data/{st.session_state['topic']}/{st.session_state['node']}"
                    st.session_state['node'] = None
                    # os.remove(f"./data/{st.session_state['topic']}/{st.session_state['node']}")
                    st.switch_page("pages/graph_view.py")

            st.write(f.read())
    except:
        st.write("Error reading file")
        # Delete the corrupted file
        os.remove(f"./data/{st.session_state['topic']}/{st.session_state['node']}")

    new_option = st.text_input("Enter a new sub-topic to learn about", value="", help="Enter the name of the new sub-topic", key="new_node")

    if new_option:
        if st.button("Deep Dive!", help="Explore this new sub-topic"):
            with open(f"./data/{st.session_state['topic']}/{st.session_state['node']}", "a") as f:
                f.write(f"\nAdditional connection [[{new_option}]]")
            st.session_state["node_parent"] = st.session_state['node']
            st.session_state["node"] = new_option
            del st.session_state["new_node"]
            del new_option
            components.html("<script>window.scrollTo(0, 0);</script>", height=0, width=0)
            # st.rerun()
            st.switch_page("pages/node_view.py")
