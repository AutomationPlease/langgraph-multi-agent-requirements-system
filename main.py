"""
Main entry point for the LangGraph Multi-Agent System.

This provides a clean CLI to interact with the Supervisor + Specialist Agents
(Requirements_Writer, Data_Analyst, Test_Case_Writer) with delegation support.
"""

from dotenv import load_dotenv
load_dotenv()

from Backups.supervisor_v1 import create_supervisor_agent
from rich.console import Console
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage

console = Console()


def main():
    """Run the interactive LangGraph Multi-Agent System."""

    # Initialize the supervisor agent
    agent = create_supervisor_agent()

    # Welcome banner
    print("=== LangGraph Multi-Agent System ===")
    print("Supervisor + Specialist Agents (Requirements_Writer, Data_Analyst, Test_Case_Writer)")
    print("Delegation & Collaboration Enabled\n")

    # Thread config for persistent memory across turns
    config = {"configurable": {"thread_id": "multi-agent-session-1"}}

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break

        if not user_input.strip():
            continue

        print("\nAgent thinking...\n")

        # Invoke the multi-agent system
        response = agent.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)

        # Get last message content
        last_message = response["messages"][-1]
        content = last_message.content if hasattr(last_message, "content") else str(last_message)

        # Clean FINAL ANSWER: prefix for better display
        if content and content.lower().strip().startswith("final answer:"):
            if ":" in content:
                content = content.split(":", 1)[1].strip()

        # Display organized
        console.print(Markdown(content))
        print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
