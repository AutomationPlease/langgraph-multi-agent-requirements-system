"""
This module defines the custom tools available to the LangGraph Agents.

Each tool is decorated with @tool from LangChain so the LLM supervisor can decide to use, or delegate to sub agent.
The tools provide the agent(s) with capabilities to:
- Search the web for external information
- Read and preview Excel/CSV files
- List files in a directory
- Perform statistical analysis on datasets

These tools are intentionally practical and focused on real-world data tasks.
"""


from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from tavily import TavilyClient
import pandas as pd
from pathlib import Path
from typing import Optional

tavily = TavilyClient()


@tool
def web_search(query: str) -> str:
    """Search the web for current information, best practices, or standards."""
    try:
        results = tavily.search(query, max_results=5)
        return f"Search results for '{query}':\n{results}"
    except Exception as e:
        return f"Web search failed: {str(e)}"


@tool
def read_file(file_path: str) -> str:
    """Read the content of a file. Supports .txt, .csv, .xlsx."""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"Error: File '{file_path}' not found."
        
        if path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
            return f"Excel file: {path.name}\nShape: {df.shape}\nColumns: {list(df.columns)}\n\nFirst 10 rows:\n{df.head(10).to_string()}"
        
        elif path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
            return f"CSV file: {path.name}\nShape: {df.shape}\nColumns: {list(df.columns)}\n\nFirst 10 rows:\n{df.head(10).to_string()}"
        
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File content ({path.name}):\n{content[:1500]}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def list_folder_files(folder_path: str, file_extension: Optional[str] = None) -> str:
    """List all files in a folder. Optionally filter by extension (e.g. '.xlsx')."""
    try:
        path = Path(folder_path)
        if not path.exists():
            return f"Error: Folder '{folder_path}' not found."
        
        files = []
        for file in path.iterdir():
            if file.is_file():
                if file_extension is None or file.suffix.lower() == file_extension.lower():
                    files.append(file.name)
        
        if not files:
            return f"No files found in '{folder_path}'."
        
        result = f"Found {len(files)} files in '{folder_path}':\n"
        for f in files[:30]:
            result += f"• {f}\n"
        if len(files) > 30:
            result += f"... and {len(files)-30} more files."
        return result
    except Exception as e:
        return f"Error listing folder: {str(e)}"


@tool
def analyze_dataframe(file_path: str) -> str:
    """Analyze a CSV or Excel file and provide insights."""
    try:
        path = Path(file_path)
        if path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
        summary = f"""
Dataset Summary for {path.name}:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Missing Values: {df.isnull().sum().sum()}

Key Statistics:
{df.describe().to_string()}

Column Names: {list(df.columns)}
"""
        return summary
    except Exception as e:
        return f"Analysis failed: {str(e)}"


@tool
def delegate_to_specialist(agent_name: str, task: str) -> str:
    """Delegate a specialized task to one of the expert agents.
    
    Use this tool when the task requires deep expertise in requirements writing,
    data analysis, or test case generation instead of using general tools.
    
    Args:
        agent_name: The specialist to delegate to. Must be exactly one of:
                   'Requirements_Writer', 'Data_Analyst', or 'Test_Case_Writer'
        task: A clear, detailed description of what the specialist should do.
    """
    valid_agents = ["Requirements_Writer", "Data_Analyst", "Test_Case_Writer"]
    
    if agent_name not in valid_agents:
        return f"Error: Invalid agent_name '{agent_name}'. Must be one of {valid_agents}"
    
    # Return a structured signal that the router can detect
    return f"DELEGATION_REQUEST|{agent_name}|{task}"
