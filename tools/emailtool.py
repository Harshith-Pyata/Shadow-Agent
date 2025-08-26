
from langchain_google_community import GmailToolkit
import os
import sys
import json


from langchain_core.tools import Tool,tool
from pydantic import BaseModel, Field
from typing import Optional,List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.llm_model import llm

toolkit = GmailToolkit()

emailtools = toolkit.get_tools()

required_tools = {tool.name: tool for tool in emailtools}

@tool
def sendmail_tool(input_model):
    """
    Sends an email with optional attachments after verifying that the attachment files exist.
    Input should be like
    {
        "to":,
        "subject":,
        "message":

    }
    """
    send_email_tool = required_tools.get("send_gmail_message")
    
    if isinstance(input_model, str):
        try:
            input_model = json.loads(input_model)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {e}")
    
    print(input_model)

    return send_email_tool.invoke(input_model)



@tool
def draftmail_tool(input_model):
    """
    drafts an email with optional attachments
    Input should be like
    {   "message":,
        "to":,
        "subject":
        

    }
    """
    print(input_model)
    draft_email_tool = required_tools["create_gmail_draft"]
    # if isinstance(input_model, str):
    #     try:
    input_model = json.loads(input_model)
        # except json.JSONDecodeError as e:
        #     raise ValueError(f"Invalid JSON input: {e}")
    
    print(input_model)
    return draft_email_tool.invoke({
        "message": input_model["message"],
        "to":[input_model["to"]],
        "subject": input_model["subject"]
    })

from enum import Enum

class Resource(str, Enum):
    """Enumerator of Resources to search."""

    THREADS = "threads"
    MESSAGES = "messages"

class SearchArgsSchema(BaseModel):
    """Input for SearchGmailTool."""

    # From https://support.google.com/mail/answer/7190?hl=en
    query: str = Field(
        ...,
        description="The Gmail query. Example filters include from:sender,"
        " to:recipient, subject:subject, -filtered_term,"
        " in:folder, is:important|read|starred, after:year/mo/date, "
        "before:year/mo/date, label:label_name"
        ' "exact phrase".'
        " Search newer/older than using d (day), m (month), and y (year): "
        "newer_than:2d, older_than:1y."
        " Attachments with extension example: filename:pdf. Multiple term"
        " matching example: from:amy OR from:david.",
    )
    resource: Resource = Field(
        default=Resource.MESSAGES,
        description="Whether to search for threads or messages.",
    )
    max_results: int = Field(
        default=10,
        description="The maximum number of results to return.",
    )

def searchmail(input: SearchArgsSchema):
    """
        search for required request based on the query in gmail
    """
    if isinstance(input, str):
        # If LLM passed raw string, wrap it into schema manually
        parsed = SearchArgsSchema(query=input)
    elif isinstance(input, dict):
        parsed = SearchArgsSchema(**input)
    else:
        parsed = input  # Already a SearchArgsSchema
    search_email_tool = required_tools["search_gmail"]
    return search_email_tool.invoke({
        "query": parsed.query,
        "max_results": parsed.max_results
    })

searchmail_tool = Tool(
    name="searchmail",
    description="""
        search for required request based on the query in gmail
    """,
    args_schema=SearchArgsSchema,
    func=searchmail
)
