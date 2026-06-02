from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import analyze_dataframe, read_file

def create_requirements_writer():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return create_react_agent(llm, tools=[], name="Requirements_Writer")

def create_data_analyst():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return create_react_agent(llm, tools=[analyze_dataframe, read_file], name="Data_Analyst")

def create_test_case_writer():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return create_react_agent(llm, tools=[], name="Test_Case_Writer")
