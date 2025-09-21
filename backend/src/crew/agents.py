import os
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from .local_tools import local_search_tool


llm = ChatGroq(
    model_name="groq/llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


symptom_classifier = Agent(
    role='Symptom Classifier',
    goal='Accurately extract and list key medical symptoms from user input.',
    backstory='You are an AI expert in medical NLP. Your job is to identify potential medical symptoms from text and list them clearly.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# condition_matcher = Agent(
#     role='Condition Matcher',
#     goal='Cross-reference symptoms with a medical knowledge base to find potential conditions.',
#     backstory='You are a highly analytical AI medical researcher. You use your tools to find conditions associated with a list of symptoms.',
#     verbose=True,
#     allow_delegation=False,
#     tools=[pubmed_tool],
#     llm=llm
# )

condition_matcher = Agent(
    role ='Condition Matcher',
    goal='Cross-reference symptoms with a medical knowledge base to find potential conditions.',
    backstory='You are a highly analytical AI medical researcher. You use your tools to find conditions associated with a list of symptoms.',
    verbose=True,
    allow_delegation=False,
    tools=[local_search_tool],
    llm=llm
)

advice_agent = Agent(
    role='Medical Advice Provider',
    goal='Provide responsible, general healthcare advice based on potential conditions.',
    backstory='You are a cautious AI healthcare assistant. You MUST always start your advice with a strong disclaimer that you are not a doctor and the user should consult a real healthcare professional.',
    verbose=True,
    allow_delegation=False,
    llm=llm
)

def create_symptom_tasks(user_input):
    # Task for the Symptom Classifier
    classify_task = Task(
        description=(
            "Analyze the user input and extract a simple, comma-separated list of medical symptoms.\n\n"
            f"USER INPUT: '{user_input}'"
        ),
        expected_output=(
            "A single, comma-separated string of symptoms ONLY. Do NOT include JSON, explanations, "
            "or any other text. Example: 'headache, fever, sore throat'"
        ),
        agent=symptom_classifier
    )

    # Task for the Condition Matcher
    match_condition_task = Task(
        description=(
            "Use the output from the previous task, which is a comma-separated string of symptoms, "
            "as the input for the Local Symptom-Disease CSV Search Tool."
        ),
        expected_output="A bulleted list of potential medical conditions based on the search results.",
        agent=condition_matcher,
        # This explicitly passes the previous task's output as an argument to this task
        context=[classify_task]
    )


    provide_advice_task = Task(
        description=(
            "Based on the list of potential conditions, provide general, non-prescriptive health advice. "
            "IMPORTANT: Start with a clear disclaimer that you are not a medical professional."
        ),
        expected_output="A paragraph containing a disclaimer and general health advice.",
        agent=advice_agent,
        context=[match_condition_task]
    )
    
    return [classify_task, match_condition_task, provide_advice_task]


def create_symptom_crew(user_input):
    tasks = create_symptom_tasks(user_input)
    return Crew(
        agents=[symptom_classifier, condition_matcher, advice_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )