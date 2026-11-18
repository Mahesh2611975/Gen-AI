from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from state import BlogState
from agents import researcher_agent, writer_agent, get_llm, editor_agent


MAX_REVISIONS = 3

#### NODE - Edges
### Defining the nodes

def reesearcher_node(state: BlogState):
    """Researcher agent generates (or revises) the research outline"""
    llm = get_llm()
    researcher_data = researcher_agent(
        llm=llm,
        topic=state.topic,
        audience=state.audience,
        feedback=state.research_feedback
    )
    state.research = researcher_data
    state.research_feedback = ""

    return state
    
def human_review_research_node(state: BlogState):
    """"pause and ask the human to approve the research or send the feedback"""
    decision = interrupt({
        "state":"reseacher_review",
        "research": state.research,
        "instructions":(
            "replay with 'approve' to continue to writting",
            "or describe what to change to send it back to the researcher."
        )
    })
    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str(decision)
        action = "approve" if text.lower() in ["approve", "ok", "yes","process"] else "revise"
        feedback = "" if action == "approve" else text

    state.research_feedback = feedback
    return state

def writer_node(state: BlogState):
    pass

def editor_node(state: BlogState):
    pass
