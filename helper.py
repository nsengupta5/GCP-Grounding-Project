from vertexai.generative_models import GenerationResponse

ENCODING = "utf-8"


def print_grounding_response(response: GenerationResponse):
    grounding_metadata = response.candidates[0].grounding_metadata

    # Citation indices are in bytes
    text_bytes = response.text.encode(ENCODING)

    prev_index = 0

    for grounding_support in grounding_metadata.grounding_supports:
        text_segment = text_bytes[prev_index : grounding_support.end_index].decode(
            ENCODING
        )
