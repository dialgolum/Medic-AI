import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field




class PubMedSearchInput(BaseModel):
    symptoms: str = Field(
        description="A comma-separated string of medical symptoms.")




class PubMedSearchTool(BaseTool):
    name: str = "PubMed Medical Search Tool"
    description: str = "Searches PubMed for medical articles related to symptoms to find potential conditions."
    args_schema: type[BaseModel] = PubMedSearchInput

    def _run(self, symptoms: str) -> str:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi"

        query = f"({symptoms.replace(',', ' AND ')}) AND (symptom OR diagnosis)"

        params = {
            "db": "pubmed", "term": query, "retmode": "json",
            "retmax": 5, "api_key": os.getenv("NCBI_API_KEY")
        }

        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            id_list = response.json().get("esearchresult", {}).get("idlist", [])

            if not id_list:
                return "No relevant medical articles found on PubMed."

            summary_url = f"{base_url}esummary.fcgi"
            summary_params = {
                "db": "pubmed", "id": ",".join(id_list),
                "retmode": "json", "api_key": os.getenv("NCBI_API_KEY")
            }
            summary_response = requests.get(summary_url, params=summary_params)
            summary_response.raise_for_status()

            results = summary_response.json().get("result", {})
            titles = [results[uid].get("title", "No Title")
                      for uid in results if uid != "uids"]
            return "\n".join(f"Title: {title}" for title in titles)
        except requests.exceptions.RequestException as e:
            return f"An error occurred while searching PubMed: {e}"



pubmed_tool = PubMedSearchTool()
