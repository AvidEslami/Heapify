import streamlit as st
import networkx as nx
from pyvis.network import Network
from collections import defaultdict
import os
from components.custom_graph import custom_graph

from tools.queries import get_initial_topic_list

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


if 'path_to_delete' in st.session_state:
    os.remove(st.session_state['path_to_delete'])
    del st.session_state['path_to_delete']

if 'topic' not in st.session_state:
    st.write("Please switch to the landing page to select a topic or graph view to select a topic and a node!")
    # Redirect buttons 
    st.button("Go to Landing", key="landing")
    if st.session_state['landing']:
        st.session_state['page'] = "Landing"
        st.switch_page("pages/landing.py")
else:
    # Check if there's a directory for ./data/{topic} and create it if it doesn't exist
    if not os.path.exists(f"./data/{st.session_state['topic']}"):
        os.makedirs(f"./data/{st.session_state['topic']}")
    elif os.path.exists(f"./data/{st.session_state['topic']}/topic_list.txt"): # Check if there's a topic_list.txt file in the directory
        with open(f"./data/{st.session_state['topic']}/topic_list.txt", "r") as f:
            topics = f.read().split("\n")

    # if topics is not defined, get the initial topic list
    if 'topics' not in locals():
        topics = get_initial_topic_list(st.session_state['topic'])
        with open(f"./data/{st.session_state['topic']}/topic_list.txt", "w") as f:
            f.write("\n".join(topics))

    def graphify_data():
        nodes = []
        edges = []
        parents = {}
        # Grab the ignored topics from the ignored_topics.txt file
        if os.path.exists(f"./data/{st.session_state['topic']}/ignored_topics.txt"):
            with open(f"./data/{st.session_state['topic']}/ignored_topics.txt", "r") as f:
                ignored_topics = f.read()
        else:
            ignored_topics = ""
        for filename in os.listdir(f"./data/{st.session_state['topic']}"):
            with open(f"./data/{st.session_state['topic']}/{filename}", "r") as f:
                if filename == "topic_list.txt" or filename == "ignored_topics.txt" or filename.replace(".md","") in ignored_topics:
                    continue
                filename = filename.replace(".md", "") # Strip .md from filename
                nodes.append(filename)
                while character := f.read(1):
                    if character == "[":
                        next_char = f.read(1)
                        if next_char == "[":
                            target_node = ""
                            next_char = f.read(1)
                            while next_char != "]":
                                target_node += next_char
                                next_char = f.read(1)
                            if "*" in target_node or (len(target_node) > 50):
                                # We drop this connection
                                continue
                            if target_node in ignored_topics:
                                continue
                            edges.append((filename, target_node))
                            parents[target_node] = filename
        return nodes, edges, parents, ignored_topics


    nodes, edges, parents, ignored_topics = graphify_data()
    # st.session_state['all_topics'] = topics + nodes
    for topic in topics:
        if topic not in ignored_topics:
            edges.append((st.session_state['topic'], topic))
            parents[topic] = st.session_state['topic']
    parents[st.session_state['topic']] = "holistically"


    uncovered_topics = []
    for edge in edges:
        if edge[1] not in nodes and edge[1] not in uncovered_topics:
            uncovered_topics.append(edge[1])
    st.session_state['all_topics'] = uncovered_topics

    def generate_graph():

        # Detect Streamlit theme
        theme = st.get_option("theme.base")
        if theme:
            is_dark = theme == "dark"
        else:
            is_dark = True

        # Set colors based on theme
        bg_color = "#2B2B2B" if is_dark else "#FAFAFA"
        font_color = "#E0E0E0" if is_dark else "#2C2C2C"
        topic_node_color = "#FF8C00" if is_dark else "#FF7043"
        explored_node_color = "#00FF00" if is_dark else "#4CAF50"
        unexplored_node_color = "#AAAAAA" if is_dark else "#B0BEC5"

        graph = nx.Graph()
        # First add the topic node
        # st.write(st.session_state['topic'])
        graph.add_node(st.session_state['topic'], label=st.session_state['topic'], color=topic_node_color, shape="dot", size=25, font={"color": font_color})

        for node in nodes:
            graph.add_node(node, label=node, color=explored_node_color, shape="dot", size=15, font={"color": font_color})

        for topic in uncovered_topics:
            graph.add_node(topic, label=topic, color=unexplored_node_color, shape="dot", size=15, font={"color": font_color})

        graph.add_edges_from(edges, length=300)
        # Custom physics for stronger repulsion

        net = Network(notebook=False, cdn_resources='remote')
        # net.set_edge_smooth('false') # OPTIONAL
        # net.show_buttons(filter_=['nodes', 'edges', 'physics'])
        # Save and inject JS to trigger a redirect with node param
        net.from_nx(graph)
        net.save_graph("test.html")
        with open("test.html", "r", encoding="utf-8") as f:
            html = f.read()
            html = html.replace("background-color: #ffffff;", f"background-color: {bg_color};") # Background color
            html = html.replace("border: 1px", f"border: 0px") # Remove border
        return html


    source_code = generate_graph()

    st.markdown(
        """
        <h1 style='text-align: left; color: #333333; font-size: 1.6vw; color: #E0E0E0; margin-bottom: 20px; padding: 0px; border-radius: 0px;'>
            Click a node to explore further!
        </h1>
        """,
        unsafe_allow_html=True
    )

    graph_option = custom_graph(elem=source_code, key="custom_graph")

    @st.dialog(graph_option if graph_option else "None")
    def NodeClick():
        st.write(f"What would you like to do?")
        col1, col2 = st.columns(2)
        with col1:    
          if st.button("Explore", use_container_width=True):
              st.session_state["node"] = graph_option
              st.session_state["node_parent"] = parents[graph_option]
              st.switch_page("pages/node_view.py")
        with col2:
          if st.button("Delete", use_container_width=True):
              # Check if node file exists
              node = graph_option
              
              st.session_state["deleter"] = True
              if os.path.exists(f"./data/{st.session_state['topic']}/{node}.md"):
                os.remove(f"./data/{st.session_state['topic']}/{node}.md")
                st.success("Node deleted.")
              else:
                # Check if this topic has an ignored_topics.txt file
                if not os.path.exists(f"./data/{st.session_state['topic']}/ignored_topics.txt"):
                    with open(f"./data/{st.session_state['topic']}/ignored_topics.txt", "w") as f:
                        f.write(node)
                else:
                    with open(f"./data/{st.session_state['topic']}/ignored_topics.txt", "r") as f:
                        # Append the node to the ignored_topics.txt file
                        ignored_topics = f.read().split("\n")
                    if node not in ignored_topics:
                        ignored_topics.append(node)
                    with open(f"./data/{st.session_state['topic']}/ignored_topics.txt", "w") as f:
                        f.write("\n".join(ignored_topics))
                # Prevent window from staying open
                # graph_option = ""
        if "deleter" in st.session_state and st.session_state["deleter"]:
            st.session_state["deleter"] = False
            del st.session_state["custom_graph"]
            st.rerun()


    if graph_option:
        NodeClick()

    option = st.selectbox("Pick an existing node:", nodes,index=None,placeholder=f"Search for Previously Explored Node. Currently selected: {st.session_state['node'] if 'node' in st.session_state else 'None'}")
    # st.write(option)
    if option:
        st.session_state["node"] = option
        st.session_state["node_parent"] = parents[option]
        st.switch_page("pages/node_view.py")

    # uncovered_topics = []
    # for topic in topics:
    #     if topic not in nodes:
    #         uncovered_topics.append(topic)
    new_option = st.selectbox("Pick a new node to learn about", uncovered_topics,index=None,placeholder=f"")

    if new_option:
        st.session_state["node"] = new_option
        st.session_state["node_parent"] = parents[new_option]
        st.switch_page("pages/node_view.py")

    # params = st.query_params
    # if "node" in params:
    #     st.session_state["node"] = params["node"]
    #     st.switch_page("pages/node_view.py")
