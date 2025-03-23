import streamlit as st
import os
from tools.queries import get_topic_lesson
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url("https://raw.githubusercontent.com/AlcxMtr/Heapify/main/static/heapify.webp");
                background-repeat: no-repeat;
                background-position: 20px 10px;
                background-size: 72px 72px;       /* 1.5x size */
                padding-top: 90px;                /* give a bit more vertical room */
            }

            [data-testid="stSidebarNav"]::before {
                content: "Heapify";
                display: block;
                font-size: 26px;
                font-weight: bold;
                margin-left: 100px;               /* shift text to the right of larger image */
                margin-top: -80px;                /* align vertically with 72px image */
                line-height: 72px;
                color: #FF8C00;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
add_logo()

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
