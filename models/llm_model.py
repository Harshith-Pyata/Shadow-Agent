import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
import azure.cognitiveservices.speech as speechsdk

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()


llm = AzureChatOpenAI(

    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    openai_api_key=os.getenv("AZURE_OPENAI_KEY")
)

chat_history = [
    SystemMessage(content="You are a helpful assistant hepls to do user actions"),
    HumanMessage(content="Give responses based on the prompt")
]
result = llm.invoke(chat_history)



def work(query):

    chat_history.append(HumanMessage(content=query))
    result = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ",result.content)

    return result.content
