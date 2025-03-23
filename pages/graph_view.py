import streamlit as st
import networkx as nx
from pyvis.network import Network
from collections import defaultdict
import os
from components.custom_graph import custom_graph

from tools.queries import get_initial_topic_list

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
    for filename in os.listdir(f"./data/{st.session_state['topic']}"):
        with open(f"./data/{st.session_state['topic']}/{filename}", "r") as f:
            if filename == "topic_list.txt":
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
                        edges.append((filename, target_node))
                        parents[target_node] = filename
    return nodes, edges, parents


nodes, edges, parents = graphify_data()
# st.session_state['all_topics'] = topics + nodes
for topic in topics:
    edges.append((st.session_state['topic'], topic))
    parents[topic] = st.session_state['topic']


uncovered_topics = []
for edge in edges:
    if edge[1] not in nodes and edge[1] not in uncovered_topics:
        uncovered_topics.append(edge[1])
st.session_state['all_topics'] = uncovered_topics

def generate_graph():
    graph = nx.Graph()
    # First add the topic node
    graph.add_node(st.session_state['topic'], label=st.session_state['topic'], color="#BF40BF", shape="dot", size=25)

    for node in nodes:
        graph.add_node(node, label=node, color="#00ff00", shape="dot", size=15)
    graph.add_edges_from(edges, length=300)
    # Custom physics for stronger repulsion

    net = Network(notebook=False, cdn_resources='remote')
    # net.set_edge_smooth('false') # OPTIONAL
    net.show_buttons(filter_=['nodes', 'edges', 'physics'])
    # Save and inject JS to trigger a redirect with node param
    net.from_nx(graph)
    net.save_graph("test.html")
    with open("test.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html

st.title("Graph pyvis test!")

source_code = generate_graph()

graph_option = custom_graph(elem=source_code, key="custom_graph")

if graph_option:
    st.session_state["node"] = graph_option
    st.session_state["node_parent"] = parents[graph_option]
    st.switch_page("pages/node_view.py")

option = st.selectbox("Pick an existing node:", nodes,index=None,placeholder=f"Currently selected: {st.session_state['node'] if 'node' in st.session_state else 'None'}")
# st.write(option)
if option:
    st.session_state["node"] = option
    st.session_state["node_parent"] = parents[option]
    st.switch_page("pages/node_view.py")

# uncovered_topics = []
# for topic in topics:
#     if topic not in nodes:
#         uncovered_topics.append(topic)
new_option = st.selectbox("Pick a new node to learn about", uncovered_topics,index=None,placeholder=f"None")

if new_option:
    st.session_state["node"] = new_option
    st.session_state["node_parent"] = parents[new_option]
    st.switch_page("pages/node_view.py")

# params = st.query_params
# if "node" in params:
#     st.session_state["node"] = params["node"]
#     st.switch_page("pages/node_view.py")
