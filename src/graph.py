from agent_state import AgentState
from nodes import *
from langgraph.graph import StateGraph, END
from sql import connect_sqlite

def should_continue(state: AgentState):
    if state.get("is_approved"):
        return "end"
    return "re-design"

def init_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("analyze", analyze_node)
    workflow.add_node("design", design_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("review", review_node)

    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "design")
    workflow.add_edge("design", "generate")
    workflow.add_edge("generate", "review")
    workflow.add_conditional_edges("review", should_continue, {"end": END, "re-design": "design"})

    checkpointer = connect_sqlite()

    app = workflow.compile(checkpointer=checkpointer)

    return app