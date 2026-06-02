from dotenv import load_dotenv
load_dotenv()


from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from state import AgentState
from tools import (
    web_search, read_file, list_folder_files, analyze_dataframe,
    delegate_to_specialist
)
from Backups.prompts import SUPERVISOR_PROMPT, AGENT_SYSTEM_PROMPTS
from agents import (
    create_requirements_writer,
    create_data_analyst,
    create_test_case_writer
)

def create_supervisor_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    # Tools available to the supervisor
    tools = [
        web_search, 
        read_file, 
        list_folder_files, 
        analyze_dataframe,
        delegate_to_specialist
    ]

    # Create specialist agents
    requirements_writer = create_requirements_writer()
    data_analyst = create_data_analyst()
    test_case_writer = create_test_case_writer()

    def supervisor_node(state: AgentState):
        system_msg = SystemMessage(content=SUPERVISOR_PROMPT)
        messages = [system_msg] + state["messages"]
        
        response = llm.bind_tools(tools).invoke(messages)
        
        # Token tracking
        tokens = 0
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            tokens = response.usage_metadata.get("total_tokens", 0)
        print(f"Supervisor Tokens: {tokens}")
        
        return {"messages": [response]}

    # Specialist agent nodes
    def requirements_writer_node(state: AgentState):
        system_msg = SystemMessage(content=AGENT_SYSTEM_PROMPTS["Requirements_Writer"])
        messages = [system_msg] + state["messages"]
        response = requirements_writer.invoke({"messages": messages})
        return {"messages": [response["messages"][-1]]}

    def data_analyst_node(state: AgentState):
        system_msg = SystemMessage(content=AGENT_SYSTEM_PROMPTS["Data_Analyst"])
        messages = [system_msg] + state["messages"]
        response = data_analyst.invoke({"messages": messages})
        return {"messages": [response["messages"][-1]]}

    def test_case_writer_node(state: AgentState):
        system_msg = SystemMessage(content=AGENT_SYSTEM_PROMPTS["Test_Case_Writer"])
        messages = [system_msg] + state["messages"]
        response = test_case_writer.invoke({"messages": messages})
        return {"messages": [response["messages"][-1]]}

    def route_supervisor(state: AgentState):
        last_message = state["messages"][-1]

        # Check if supervisor called the delegate_to_specialist tool
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                if tool_call.get("name") == "delegate_to_specialist":
                    args = tool_call.get("args", {})
                    agent_name = args.get("agent_name", "")
                    
                    print(f"Delegation tool called → Routing to {agent_name}")
                    
                    if agent_name == "Requirements_Writer":
                        return "requirements_writer"
                    elif agent_name == "Data_Analyst":
                        return "data_analyst"
                    elif agent_name == "Test_Case_Writer":
                        return "test_case_writer"
        
        # Check for final answer in regular text response
        content = ""
        if hasattr(last_message, "content") and last_message.content:
            content = last_message.content.lower()
        
        if "final answer:" in content:
            print("Final answer detected - ending workflow")
            return END
        
        # Default: use tools or end
        return tools_condition(state)

    # Build the graph
    workflow = StateGraph(AgentState)
    
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("requirements_writer", requirements_writer_node)
    workflow.add_node("data_analyst", data_analyst_node)
    workflow.add_node("test_case_writer", test_case_writer_node)

    workflow.add_edge(START, "supervisor")
    
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "tools": "tools",
            "requirements_writer": "requirements_writer",
            "data_analyst": "data_analyst",
            "test_case_writer": "test_case_writer",
            END: END
        }
    )
    
    workflow.add_edge("tools", "supervisor")
    workflow.add_edge("requirements_writer", "supervisor")
    workflow.add_edge("data_analyst", "supervisor")
    workflow.add_edge("test_case_writer", "supervisor")

    memory = InMemorySaver()
    return workflow.compile(checkpointer=memory)
