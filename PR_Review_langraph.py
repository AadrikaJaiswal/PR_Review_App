import os
import requests
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv("groq_api_key")
langsmith_api_key = os.getenv("langsmith_api_key")
github_token = os.getenv("github_token")

os.environ["LANGCHAIN_API_KEY"] = langsmith_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "PR_Review_App"

llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

class PR_State(TypedDict):
    pr_url: str
    pr_details: dict
    summary: str
    issues: str
    comments: str

graph_builder = StateGraph(PR_State)

def fetch_pr_details(state: PR_State):
    pr_url = state["pr_url"]
    
    try:
        parts = pr_url.rstrip("/").split("/")
        owner, repo, pr_number = parts[-4], parts[-3], parts[-1]
    except IndexError:
        return {"pr_details": {"error": "Invalid PR URL"}}

    headers = {"Authorization": f"token {github_token}"}
    pr_api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    response = requests.get(pr_api_url, headers=headers)
    
    if response.status_code != 200:
        return {"pr_details": {"error": "Failed to fetch PR details"}}

    pr_data = response.json()
    return {"pr_details": pr_data}

graph_builder.add_node("fetch_pr_details", fetch_pr_details)

def pr_summary(state: PR_State):
    pr_details = state["pr_details"]
    
    if "error" in pr_details:
        return {"summary": pr_details["error"]}

    pr_title = pr_details.get("title", "Unknown Title")
    diff_url = pr_details.get("diff_url", "")

    summary_prompt = f"Summarize the key changes in this PR titled '{pr_title}'. Changes: {diff_url}"
    summary = llm.invoke(summary_prompt)

    return {"summary": summary.content}

graph_builder.add_node("pr_summary", pr_summary)

def detect_issues(state: PR_State):
    summary = state["summary"]

    issue_prompt = f"Identify any potential coding issues or improvements in the following PR summary: {summary}"
    issues = llm.invoke(issue_prompt)

    return {"issues": issues.content}

graph_builder.add_node("detect_issues", detect_issues)

def pr_comments(state: PR_State):
    issues = state["issues"]

    comment_prompt = f"Based on these issues: {issues}, generate comments for GitHub PR review."
    comments = llm.invoke(comment_prompt)

    return {"comments": comments.content}

graph_builder.add_node("pr_comments", pr_comments)

graph_builder.add_edge(START, "fetch_pr_details")
graph_builder.add_edge("fetch_pr_details", "pr_summary")
graph_builder.add_edge("pr_summary", "detect_issues")
graph_builder.add_edge("detect_issues", "pr_comments")
graph_builder.add_edge("pr_comments", END)

graph = graph_builder.compile()