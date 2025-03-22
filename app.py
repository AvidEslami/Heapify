import streamlit as st

graph_view = st.Page("pages/graph_view.py", title="Graph View", icon="🤓")
node_view = st.Page("pages/node_view.py", title="Node View", icon="🤓")
landing = st.Page("pages/landing.py", title="Topic Selection", icon="🐩")

pg = st.navigation({"Start":[landing], "Data":[graph_view, node_view]})
st.session_state['page'] = pg.run()
# pg.run()