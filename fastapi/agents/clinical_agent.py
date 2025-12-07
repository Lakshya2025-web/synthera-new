from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json
from .state import State
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
def clinical_node(state: State):
    query = state.user_input
    prompt = f"""
You are a Clinical Trials Intelligence Agent simulating data from ClinicalTrials.gov and WHO ICTRP.

Generate synthetic but realistic clinical trial pipeline data.

STRICT RULES:
- Output ONLY RAW JSON.
- NO markdown.
- NO backticks.
- NO explanation text.
- Follow EXACTLY this structure:

{{
  "active_trials": [
    {{
      "nct_id": "NCT01234567",
      "title": "",
      "condition": "",
      "phase": "Phase 1|Phase 2|Phase 3|Phase 4",
      "status": "Recruiting|Active|Completed",
      "sponsor": "",
      "enrollment": <number>
    }}
  ],
  "sponsor_summary": [
    {{
      "sponsor": "",
      "trials": <number>,
      "type": "Industry|Academic|Government"
    }}
  ],
  "phase_distribution": [
    {{"phase": "Phase 1", "count": <number>}},
    {{"phase": "Phase 2", "count": <number>}},
    {{"phase": "Phase 3", "count": <number>}},
    {{"phase": "Phase 4", "count": <number>}}
  ]
}}

User Query:
{query}
"""
    raw = llm.invoke(prompt).content.strip()
    if raw.startswith("```"):
        raw = raw.replace("```json", "").replace("```", "").strip()
    return {"clinical" : raw}
