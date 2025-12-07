from .state import State
import os, requests
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_key)
import requests

def pubmed_search(query: str, max_results: int = 5):
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    search_resp = requests.get(search_url, params=search_params, timeout=10).json()
    pmids = search_resp.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return []
    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    summary_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json"
    }

    summary_resp = requests.get(summary_url, params=summary_params, timeout=10).json()
    summaries = summary_resp.get("result", {})
    results = []
    for pmid in pmids:
        data = summaries.get(pmid)
        if not data:
            continue

        title = data.get("title", "Untitled Publication")
        source = data.get("source", "").strip()
        url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        snippet = f"{title}. {source}."
        results.append({
            "title": title,
            "url": url,
            "snippet": snippet,
            "source_type": "publication"
        })

    return results

def web_search(query:str):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "no_redirect": 1
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    results = []
    if data.get("AbstractText"):
        results.append({
            "title": data.get("Heading", "Summary"),
            "url": data.get("AbstractURL", ""),
            "snippet": data.get("AbstractText", ""),
            "source_type": "summary"
        })
    for item in data.get("RelatedTopics", []):
        if "Text" in item and "FirstURL" in item:
            results.append({
                "title": item["Text"][:60] + "...",
                "url": item["FirstURL"],
                "snippet": item["Text"],
                "source_type": "web"
            })
    return results


def web_node(state: State):
    query = state.user_input
    web_results = web_search(query)
    pubmed_results =pubmed_search(query)
    results = web_results + pubmed_results
    if not results:
        results = [
            {
                "title": "No real-time result found",
                "url": "",
                "snippet": "No credible public search result was found for this query.",
                "source_type": "fallback"
            }
        ]   
    context_lines = []
    for r in results:
        if r["url"]:
            line = f"- [{r['title']}]({r['url']}) ({r['source_type']}): {r['snippet']}"
        else:
            line = f"- {r['title']} ({r['source_type']}): {r['snippet']}"
        context_lines.append(line)
    context_block = "\n".join(context_lines)
    prompt = f"""
You are a Web Intelligence Agent specializing in pharma, clinical, and biomedical research.

Below are REAL online search results (DuckDuckGo + PubMed) related to:

{query}

Search Results:
{context_block}

TASK:
- Write a multi-paragraph web intelligence summary.
- Include bullet points and hyperlinks.
- Quote exact lines from sources using quotation marks.
- Distinguish clearly between:
  * Guidelines
  * Scientific publications (especially PubMed)
  * News
  * Patient forums
- Do NOT invent URLs. Use only the ones provided.

Return ONLY a Markdown summary.
"""
    summary = llm.invoke(prompt).content.strip()
    return {"web": summary}
