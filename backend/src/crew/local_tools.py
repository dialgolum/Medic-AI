# src/symptom_checker/crew/local_tools.py
import pandas as pd
from pathlib import Path
from crewai.tools import tool

@tool("Local Symptom-Disease CSV Search Tool")
def local_search_tool(symptoms: str) -> str:
    """Searches a local CSV file to find diseases matching a list of symptoms. 
    The input to this tool should be a single, comma-separated string of symptoms."""
    try:
        # Build a reliable path to the data file
        script_dir = Path(__file__).resolve().parent.parent
        data_path = script_dir / "data" / "symptom_disease.csv"
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        return "Error: The symptom_disease.csv file was not found."

    symptom_list = [s.strip().lower() for s in symptoms.split(',')]
    matching_diseases = []

    for index, row in df.iterrows():
        csv_symptoms = set(s.strip().lower() for s in row['symptoms'].split(','))
        if any(s in csv_symptoms for s in symptom_list):
            matching_diseases.append(row['disease'])

    if not matching_diseases:
        return "No matching diseases found in local data for the provided symptoms."

    return f"Found potential matches in local data: {', '.join(matching_diseases)}"