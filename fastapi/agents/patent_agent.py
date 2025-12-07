from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json
from .state import State
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
def patent_node(state: State):
    query = state.user_input
    prompt = f"""
You are a Patent Intelligence Agent simulating USPTO/Derwent/Clarivate patent data.

Generate synthetic but realistic patent landscape analytics.

STRICT RULES:
- Output ONLY raw JSON (no markdown, no ```json).
- No explanations.
- Follow EXACTLY this structure:

{{
  "patents": [
    {{
      "patent_number": "",
      "assignee": "",
      "priority_year": <number>,
      "filing_year": <number>,
      "expiry_year": <number>,
      "status": "active|expired|pending",
      "fto_risk": "low|medium|high"
    }}
  ],
  "expiry_timeline": [
    {{"year": <year>, "count": <number>}},
    {{"year": <year>, "count": <number>}}
  ],
  "competitive_heatmap": [
    {{"company": "", "score": <0-10>}},
    {{"company": "", "score": <0-10>}}
  ],
  "excerpts": [
    "",
    ""
  ]
}}

User Query:
{query}
"""
    res = llm.invoke(prompt).content.strip()
    if res.startswith("```"):
        res = res.replace("```json", "").replace("```", "").strip()
    return {"patent": res}
