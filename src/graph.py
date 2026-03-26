from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
from schema import NodeName, Route
from nodes import pm_node, architect_node, developer_node, coordinator_node
from agent_state import AgentState
from sql import connect_sqlite

def decide_finish(state: AgentState) -> Route:
    if state.get("is_approved") is True:
        return Route.END
    return Route.RE_ARCHITECT

def check_requirements(state: AgentState) -> Route:
    reqs = state.get("requirements")
    if reqs and reqs.is_info_sufficient:
        return Route.CONTINUE
    return Route.ASK_MORE

def init_graph():
    standard_retry = RetryPolicy(max_attempts=3)

    workflow = StateGraph(AgentState)

    workflow.add_node(NodeName.PM, pm_node, retry_policy=standard_retry)
    workflow.add_node(NodeName.ARCHITECT, architect_node, retry_policy=standard_retry)
    workflow.add_node(NodeName.DEVELOPER, developer_node, retry_policy=standard_retry)
    workflow.add_node(NodeName.COORDINATOR, coordinator_node, retry_policy=standard_retry)

    workflow.add_edge(START, NodeName.PM)

    workflow.add_conditional_edges(
        NodeName.PM,
        check_requirements,
        {
            Route.CONTINUE: NodeName.ARCHITECT,
            "ask_more": END
        }
    )
    workflow.add_edge(NodeName.ARCHITECT, NodeName.DEVELOPER)
    workflow.add_edge(NodeName.DEVELOPER, NodeName.COORDINATOR)

    workflow.add_conditional_edges(
        NodeName.COORDINATOR,
        decide_finish,
        {
            Route.END: END,
            Route.RE_ARCHITECT: NodeName.ARCHITECT
        }
    )

    return workflow.compile(checkpointer=connect_sqlite())
