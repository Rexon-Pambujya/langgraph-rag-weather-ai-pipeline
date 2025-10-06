from langsmith import Client
from langsmith.evaluation import evaluate
from langsmith.schemas import Example

from src.config import Config

def run_langsmith_evaluation(prompt_fn, dataset_examples:list[dict], project_name:str = "langgraph-rag-weather"):
    """
    prompt_fn: a function that takes example input and returns a LLM output (the target fuction)
    dataset_examples: a list of dictionaries with 'input' and 'output' keys
    """
    Client = Client(api_key=Config.LANGSMITH_API_KEY)

    examples = [Example(input=ex['input'], output=ex['output']) for ex in dataset_examples]

    evaluation = evaluate(
        target_fn = prompt_fn,
        examples = examples,
        client=Client,
        project_name=project_name
    )

    return evaluation