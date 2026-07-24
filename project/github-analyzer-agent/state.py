from typing import TypedDict

class AgentState(TypedDict):
    github_url : str
    files :list[str]
    files_content : dict
    analysis :str
    report:str
    selected_file:str
