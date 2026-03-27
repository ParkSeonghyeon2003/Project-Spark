from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from schema import PMOutput, ArchitectOutput, DeveloperOutput

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    requirements: Optional[PMOutput]
    tech_stack: Optional[ArchitectOutput]
    file_structure: Optional[DeveloperOutput]
    is_approved: bool
    feedback: Optional[str]