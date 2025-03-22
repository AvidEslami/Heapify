import streamlit as st
import networkx as nx
from pyvis.network import Network

# st.write("This is a simple Streamlit app.")

nodes = ["Note A", "Note B", "Note C"]
edges = [("Note A", "Note B"), ("Note B", "Note C")]

graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

net = Network(notebook=True, cdn_resources='remote')
net.from_nx(graph)

st.title("Graph pyvis test!")

net.save_graph("test.html")
HtmlFile = open("test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
st.components.v1.html(source_code, height=600, width=800)

# with open(r"C:\Users\avide\Documents\Obsidian Vault\Side Projects\DryWorld.md", "r") as f:
#     content = f.read()

# st.markdown(content)