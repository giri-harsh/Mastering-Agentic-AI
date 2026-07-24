from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from state import AgentState
from tools import get_repo_files,get_file_content
from langgraph.graph import StateGraph,START,END
from typing import TypedDict
import os

load_dotenv()
llm = ChatGroq(
    model = "llama-3.3-70b-versatile",api_key=os.getenv('GROQ_API_KEY')
)

def fetch_repo(state:AgentState):
    token = os.getenv("GITHUB_TOKEN")
    files = get_repo_files(state['github_url'],token)
    return {"files":files}

def read_file(state:AgentState):
    token = os.getenv("GITHUB_TOKEN")
    file_contents = {}
    for filename in state['files']:
        try :
            content = get_file_content(state['github_url'],filename,token)
            file_contents[filename]= content
        except :
            file_contents [filename] = "Could not load content"
    return {"file_contents": file_contents}

def analyze(state:AgentState):
    code_summary =""
    for filename,content in state['files_content'].items():
        code_summary += f"\n\n--- {filename} ---\n{content[:500]}"
    prompt = f"""Analyze this GitHub repository code and provide:
    1. What this project does
    2. Main technologies used
    3. Issues or bugs found
    4. Suggestions for improvement

    Code: 
    {code_summary}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"analysis": response.content}



# #  NEXT UP :
# This looks good. Now write generate_report yourself:

# It's the simplest node:

# Takes analysis and github_url from state
# Formats a clean readable report string
# Returns {"report": report}