# src/agent/graph.py
# ==============================================
# 👨‍🍳 The Head Chef (Orchestrator)
# This file builds the workflow graph. It tells
# the kitchen WHAT to do next, not HOW to do it.
# All the actual work lives in nodes.py and
# the integration modules.
# ==============================================

from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    classify_node,
    validate_node,
    save_node,
    dispatch_node,
    notify_node,
    reply_node,
    mark_read_node,
)


def should_continue(state: AgentState) -> str:
    """If any step sets an error, stop cooking and send the dish back."""
    if state.get("error"):
        return "error"
    return "continue"


def build_graph():
    workflow = StateGraph(AgentState)

    # Add all kitchen stations
    workflow.add_node("classify", classify_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("dispatch", dispatch_node)
    workflow.add_node("save", save_node)
    workflow.add_node("notify", notify_node)
    workflow.add_node("reply", reply_node)
    workflow.add_node("mark_read", mark_read_node)

    workflow.set_entry_point("classify")

    # Wire stations in order, with a safety valve at each
    workflow.add_conditional_edges(
        "classify", should_continue, {"continue": "validate", "error": END}
    )

    workflow.add_conditional_edges(
        "validate", should_continue, {"continue": "dispatch", "error": END}
    )

    workflow.add_conditional_edges(
        "dispatch", should_continue, {"continue": "save", "error": END}
    )
    workflow.add_conditional_edges(
        "save", should_continue, {"continue": "notify", "error": END}
    )
    workflow.add_conditional_edges(
        "notify", should_continue, {"continue": "reply", "error": END}
    )
    workflow.add_conditional_edges(
        "reply", should_continue, {"continue": "mark_read", "error": END}
    )
    workflow.add_edge("mark_read", END)

    return workflow.compile()


def process_email(email_data: dict):
    """Run the full kitchen pipeline for one order (email)."""
    graph = build_graph()
    state = {
        "email_id": email_data["id"],
        "thread_id": email_data["threadId"],
        "tenant_email": email_data["from"],
        "email_body": email_data["body"],
        "maintenance_request": None,
        "contractor_name": None,
        "contractor_phone": None,
        "request_id": None,
        "error": None,
    }
    return graph.invoke(state)
