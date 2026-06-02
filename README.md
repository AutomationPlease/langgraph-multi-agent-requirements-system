# LangGraph Multi-Agent System

A multi-agent system built with LangGraph that can handle requirements engineering, data analysis, and test case generation by intelligently delegating work between specialized agents.

Instead of one big agent trying to do everything, this system uses a Supervisor that decides when to use tools and when to hand off work to expert agents (Requirements_Writer, Data_Analyst, and Test_Case_Writer). The delegation happens through a proper tool call rather than hoping the model outputs the right text.

This project was built to explore more advanced multi-agent patterns in LangGraph while keeping the architecture clean and maintainable.

## What This Project Demonstrates

- Building a supervisor + specialist agent architecture with LangGraph
- Using tool-based delegation instead of fragile text matching
- Creating specialized agents with focused roles and stronger prompts
- Combining general tools with expert agents in one system
- Maintaining conversation memory across multiple agent handoffs
- Structuring a real multi-agent workflow that feels practical

## Demo

```text
You: What are the files in this folder? C:\Users\Desktop\Data

Agent thinking...

Supervisor Tokens: 655
Total Tokens: 721
Final answer detected - ending workflow

The files in the folder are:                                                                                                                                                                     
 • Data Set - Copy.xlsx
 • Data Set.xlsx              

→ Supervisor determines task is easy, returns output.

======================================================================

You: What is the current weather in Dallas, Texas?

Agent thinking...

Supervisor Tokens: 757
Total Tokens: 1752
Final answer detected - ending workflow

The current weather in Dallas, Texas is 33.5°C (92.2°F) and sunny, with a wind speed of 14.8 mph. The humidity is at 53%.

→ Supervisor determines task is easy, returns output.

======================================================================

You: Please give statistical analysis for Data Set file.

Agent thinking...

Supervisor Tokens: 1797
Routing to Data_Analyst (delegation detected)
Total Tokens: 2707
Final answer detected - ending workflow

The statistical analysis of the "Data Set.xlsx" reveals significant insights regarding inventory and demand metrics. Key findings include:
• On-Hand Inventory (ON_HAND):  
Mean: 1327.82, Min: 78, Max: 6203, Standard Deviation: 1218.19  
• Week To Date Demand (WTD_DMD):  
Mean: 185.36, Min: 0, Max: 905, Standard Deviation: 204.46  
• 2-Week Demand (2WK_DMD):  
Mean: 314.14, Min: 0, Max: 1312.5, Standard Deviation: 268.35  
• 6-Week Demand (6WK_DMD):  
Mean: 352.24, Min: 0, Max: 1696.9, Standard Deviation: 335.64  
• Next On Order (NX_ON_ORDER):  
Mean: 14,662,590, Min: 10,014,320, Max: 16,018,350, Standard Deviation: 2,530,815

Trends and Recommendations:
1 Inventory Management: Improve controls to reduce variability in on-hand inventory.
2 Data Quality Improvement: Address missing values to enhance analysis reliability.
3 Demand Forecasting: Refine models using historical data for better accuracy.
4 Supply Chain Optimization: Evaluate processes for timely replenishment.                                                                                                                       
These insights can help optimize inventory management and enhance supply chain efficiency.


→ Supervisor determines task from conversation memory, delegates task to sub agent, returns final output.
```

## Key Features

- Supervisor that can delegate work using a dedicated delegate_to_specialist tool and knows when to delegate.
- Three specialized agents with focused expertise
- Support for file analysis, web search, and dataframe operations
- Persistent conversation memory within a session
- Clean CLI with nice Markdown formatting
- Clear separation between general tools and expert agents

## Tech Stack

- LangGraph + LangChain
- OpenAI (gpt-4o for specialists, gpt-4o-mini for supervisor)
- Tavily for web search
- Pandas + OpenPyXL for data handling
- uv for dependency management

## Project Structure
```text
langgraph-multi-agent-system/
├── agents.py           # Creates the specialist agents
├── main.py             # CLI interface
├── prompts.py          # System prompts for supervisor and specialists
├── state.py            # Shared state definition
├── supervisor.py       # Supervisor logic + routing
├── tools.py            # Tools including delegate_to_specialist
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

## Getting Started
```bash
# clone repo
git clone https://github.com/your-username/langgraph-multi-agent-system.git

# go to project folder
cd langgraph-multi-agent-system

# sync dependencies
uv sync

# activate venv if not already
.venv\Scripts\activate

# update .env.example to .env and add your API keys
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

# run with
uv run python main.py
```

## Current Status
This is a working multi-agent system with reliable delegation. I moved away from text-based delegation because it was inconsistent, and switched to using a proper 'delegate_to_specialist tool'. The quality of responses improved noticeably once the specialists were given stronger prompts and access to tools.
It’s still a command-line tool for now, but the architecture is solid enough that it could be extended into an API or web interface later.

## Things I’m thinking about adding:

- Giving the Data Analyst more code execution tools for more advanced analysis
- Better structured output from the specialists
- Making it easier to add new specialist agents
- Adding task automation agents

## Skills & Learnings
**Working on this helped me understand:**

- How much more reliable tool-based delegation is compared to text matching
- The importance of giving specialist agents strong, focused prompts
- How to structure state and routing in a multi-agent LangGraph workflow
- Balancing flexibility with control when designing agent systems
- Why separating concerns between a supervisor and specialists makes the system easier to reason about and improve
