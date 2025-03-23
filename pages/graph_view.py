import streamlit as st
import networkx as nx
from pyvis.network import Network
import os
import streamlit.components.v1 as components
from components.custom_graph import custom_graph

from tools.queries import get_initial_topic_list

# Check if there's a directory for ./data/{topic} and create it if it doesn't exist
if not os.path.exists(f"./data/{st.session_state['topic']}"):
    os.makedirs(f"./data/{st.session_state['topic']}")
elif os.path.exists(f"./data/{st.session_state['topic']}/topic_list.txt"): # Check if there's a topic_list.txt file in the directory
    with open(f"./data/{st.session_state['topic']}/topic_list.txt", "r") as f:
        topics = f.read().split("\n")
else:
    topics = get_initial_topic_list(st.session_state['topic'])
    with open(f"./data/{st.session_state['topic']}/topic_list.txt", "w") as f:
        f.write("\n".join(topics))

def graphify_data():
    nodes = []
    edges = []
    for filename in os.listdir(f"./data/{st.session_state['topic']}"):
        with open(f"./data/{st.session_state['topic']}/{filename}", "r") as f:
            if filename == "topic_list.txt":
                continue
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
    return nodes, edges

nodes, edges = graphify_data()

for topic in topics:
    if topic not in nodes:
        edges.append((st.session_state['topic'], topic))

graph = nx.Graph()
# First add the topic node
graph.add_node(st.session_state['topic'], label=st.session_state['topic'], color="#ff0000", shape="dot", size=15)

for node in nodes:
    graph.add_node(node, label=node, color="#00ff00", shape="dot", size=15)
graph.add_edges_from(edges)

net = Network(notebook=False, cdn_resources='remote')
net.from_nx(graph)

st.title("Graph pyvis test!")

# Save and inject JS to trigger a redirect with node param
net.save_graph("test.html")
with open("test.html", "r", encoding="utf-8") as f:
    html = f.read()

# # Inject script to update top-level window location
# html = html.replace(
#     "</body>",
#     """
#     <script type="text/javascript">
#         network.on("click", function (params) {
#             if (params.nodes.length > 0) {
#                 let nodeId = params.nodes[0];
#             }
#         });
#     </script>
#     </body>
#     """
# )

graph_option = custom_graph("custom_graph", elem=html, key="custom_graph")

if graph_option:
    st.session_state["node"] = graph_option
    st.switch_page("pages/node_view.py")

option = st.selectbox("Pick an existing node:", nodes,index=None,placeholder=f"Currently selected: {st.session_state['node'] if 'node' in st.session_state else 'None'}")
# st.write(option)
if option:
    st.session_state["node"] = option
    st.switch_page("pages/node_view.py")

uncovered_topics = []
for topic in topics:
    if topic not in nodes:
        uncovered_topics.append(topic)
new_option = st.selectbox("Pick a new node to learn about", uncovered_topics,index=None,placeholder=f"None")

if new_option:
    st.session_state["node"] = new_option
    st.switch_page("pages/node_view.py")

# params = st.query_params
# if "node" in params:
#     st.session_state["node"] = params["node"]
#     st.switch_page("pages/node_view.py")
