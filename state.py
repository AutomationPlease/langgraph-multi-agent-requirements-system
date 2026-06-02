from typing import TypedDict, List, Dict, Optional, Any, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """State for the multi-agent Requirements Engineering system"""
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Memory / Context
    current_folder: Optional[str]
    known_files: List[str]
    
    # Requirements Engineering artifacts
    requirements: Dict[str, Any]
    user_stories: List[Dict]
    test_cases: List[Dict]
    
    analysis_results: Dict[str, Any]
    final_output: Optional[str]
    
    total_tokens: int
    total_cost: float
