from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

def create_requirements_writer():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return create_react_agent(llm, tools=[], name="Requirements_Writer")

def create_data_analyst():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return create_react_agent(llm, tools=[], name="Data_Analyst")

def create_test_case_writer():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return create_react_agent(llm, tools=[], name="Test_Case_Writer")
