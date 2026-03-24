import streamlit as st

from graph import init_graph

@st.cache_resource
def load_graph():

    graph = init_graph()

    return graph