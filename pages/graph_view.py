import streamlit as st
import networkx as nx
from pyvis.network import Network
import os
import streamlit.components.v1 as components

def graphify_data():
    nodes = []
    edges = []
    for filename in os.listdir("./data"):
        with open(f"./data/{filename}", "r") as f:
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

graph = nx.Graph()
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

# Inject script to update top-level window location
html = html.replace(
    "</body>",
    """
    <script type="text/javascript">
        network.on("click", function (params) {
            if (params.nodes.length > 0) {
                const clickedNode = params.nodes[0];
                localStorage.setItem("selected_node", clickedNode);
                window.location.href = "/?node=" + clickedNode;
            }
        });
    </script>
    </body>
    """
)


with open("test.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("test.html", 'r', encoding='utf-8') as HtmlFile:
    source_code = HtmlFile.read()
components.html(source_code, height=600, width=800)

params = st.query_params
if "node" in params:
    st.session_state["node"] = params["node"]
    st.switch_page("pages/node_view.py")
