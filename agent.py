
from models.llm_model import llm
from models.text_voice import generate_audio

from langchain.agents import create_react_agent,AgentExecutor

from langchain import hub

prompt = hub.pull("hwchase17/react")

from tools.whatsapp import open_whatsapp,whatsapp_search,starts_conversation,close_whatsapp,sending_files
from tools.filesender import copy,save_text
from tools.emailtool import sendmail_tool,draftmail_tool,searchmail_tool
from tools.folder import search_files,create_folder,open_folder


agent_tools = [
    open_whatsapp,
    whatsapp_search,
    starts_conversation,
    close_whatsapp,
    sending_files,
    search_files,
    create_folder,
    open_folder,
    copy,
    save_text,
    sendmail_tool,
    draftmail_tool,
    searchmail_tool
]


agent = create_react_agent(
    llm=llm,
    tools=agent_tools,
    prompt=prompt
) 
agent_executor = AgentExecutor(
    agent=agent,
    tools=agent_tools,
    verbose=True,
    handle_parsing_errors=True
)

# Step 5: Invoke
def action(text:str):
    response = agent_executor.invoke({"input": text})
    print(response['output'])
    generate_audio(response['output'])
    