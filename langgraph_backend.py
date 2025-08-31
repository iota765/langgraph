from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
import os
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is not None:
	os.environ["GROQ_API_KEY"] = groq_api_key
else:
	raise ValueError("GROQ_API_KEY environment variable is not set.")

llm = ChatGroq(model="gemma2-9b-it", temperature=0.1, max_tokens=2000, stop_sequences=[])

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
	
def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':[response]}

checkpointer=MemorySaver()
graph=StateGraph(ChatState)

graph.add_node('chat_node',chat_node)
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)


chatbot=graph.compile(checkpointer=checkpointer)
