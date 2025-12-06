from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Literal, Optional 
import json
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
class State(BaseModel):
    user_input : str 
    route : Optional[Literal["orchestrator", "internal"]] = None 
    response : Optional[str] = None 

def master_node(state: State):
    user_input = state.user_input
    prompt = f"""
You are the MASTER AGENT for a pharma analytics system.

Your job:
1. Understand the user's query.
2. Decide whether it requires:
   - external market/clinical/patent/web intelligence → route = "orchestrator"
   - internal document or PDF summarization → route = "internal"

ROUTES:
- "orchestrator" → use when the user asks about markets, competitors, patents,
  clinical trials, guidelines, news, opportunities, etc.
- "internal" → use ONLY when the query clearly refers to internal documents,
  internal strategy decks, field reports, PDFs, or "our internal data".

User query:
{user_input!r}

RULES:
- Choose "internal" ONLY if the user explicitly mentions internal documents,
  strategy decks, internal reports, PDFs, or clearly internal content.
- In all other cases, choose "orchestrator".

RESPONSE FORMAT (STRICT):
Return ONLY a single JSON object, no extra text:

For orchestrator route:
{{"route": "orchestrator"}}

For internal route:
{{"route": "internal"}}
"""
    res = llm.invoke(prompt)
    raw = res.content
    try:
        data = json.loads(raw)
    except Exception:
        data = {"route" : "orchestrator"}
    route = data.get("route", "orchestrator")
    if route not in ("orchestrator" , "internal"):
        route = "orchestrator"
    return {"route" : route}

def orchestrator_node(state : State):
    return {"response" : "ORCHESTRATOR MODE ON"}
def internal_node(state: State):
    return {"response" : "INTERNAL MODE ON"}

graph = StateGraph(State)
graph.add_node("master", master_node)
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("internal", internal_node)
graph.set_entry_point("master")
graph.add_edge("orchestrator", END)
graph.add_edge("internal", END)
graph.add_conditional_edges("master", lambda state: state.route, {"orchestrator" : "orchestrator", "internal" : "internal"})
app = graph.compile()
user_inp = input("enter: ")
final_res = app.invoke({"user_input": user_inp})
print(final_res)

