from helper import print_grounding_response
from vertexai.generative_models import (
    GenerationResponse,
    GenerativeModel,
    Tool,
    grounding,
)
from vertexai.preview.generative_models import grounding as preview_grounding

DATASTORE_NAME = "data-intensive-store"
DATASTORE_ID = f"{DATASTORE_NAME}-id"
MODEL = "gemini-1.5-flash"
PROMPT = "Who wrote FedAdapt?"
PROJECT_ID = "summitdemo-439619"
LOCATION = "global"


def generate_without_grounding(
    model: GenerativeModel, prompt: str
) -> GenerationResponse:
    response = model.generate_content(prompt)
    print_grounding_response(response)
    return response


def generate_with_google_grounding(
    model: GenerativeModel, prompt: str
) -> GenerationResponse:
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    response = model.generate_content(prompt, tools=[tool])
    print_grounding_response(response)
    return response


def generate_with_vertex_ai_grounding(
    model: GenerativeModel, prompt: str
) -> GenerationResponse:
    tool = Tool.from_retrieval(
        preview_grounding.Retrieval(
            preview_grounding.VertexAISearch(
                datastore=DATASTORE_ID, project=PROJECT_ID, location=LOCATION
            )
        )
    )
    response = model.generate_content(prompt, tools=[tool])
    print_grounding_response(response)
    return response


if __name__ == "__main__":
    model = GenerativeModel(MODEL)
    response = generate_without_grounding(model, PROMPT)
    response = generate_with_google_grounding(model, PROMPT)
    response = generate_with_vertex_ai_grounding(model, PROMPT)
