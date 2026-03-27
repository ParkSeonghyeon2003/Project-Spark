import streamlit as st
from langchain_core.messages import AIMessage
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from graph import init_graph


@st.cache_resource
def load_graph():

    graph = init_graph()

    return graph


def run_agent_workflow(graph, input_messages, config):
    for event in graph.stream(
        {"messages": input_messages}, 
        config, 
        stream_mode="values"
    ):
        if "messages" in event:
            last_msg = event["messages"][-1]
            if isinstance(last_msg, AIMessage):
                yield last_msg


def create_project_zip(file_structure: list):
    buf = BytesIO()
    with ZipFile(buf, "w", ZIP_DEFLATED) as zf:
        for f in file_structure:
            zf.writestr(f.path, f.content)

    return buf.getvalue()

