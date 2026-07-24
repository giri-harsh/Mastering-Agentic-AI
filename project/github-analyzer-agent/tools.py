import requests
from dotenv import load_dotenv
import os
import base64


token = os.getenv("GITHUB_TOKEN")

def get_repo_files (github_url,token):
    parts = github_url.split("/")
    owner = parts[3]
    repo = parts[4]
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {'Authorization':f"token {token}"}
    response = requests.get(url,headers=headers)
    data=response.json ()
    return [item["name"] for item in data if item["type"] == "file"]

def get_file_content(github_url,filename,token):
    parts = github_url.split("/")
    owner = parts[3]
    repo = parts[4]
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filename}"
    headers = {'Authorization':f"token {token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content