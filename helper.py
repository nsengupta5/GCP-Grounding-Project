from vertexai.generative_models import GenerationResponse

ENCODING = "utf-8"


def print_grounding_response(response: GenerationResponse):
    grounding_metadata = response.candidates[0].grounding_metadata

    # Citation indices are in bytes
    text_bytes = response.text.encode(ENCODING)

    prev_index = 0

    for grounding_support in grounding_metadata.grounding_supports:
        text_segment = text_bytes[
            prev_index : grounding_support.segment.end_index
        ].decode(ENCODING)

        footnotes_text = " "
        for grounding_chunk_index in grounding_support.grounding_chunk_indices:
            footnotes_text += f"[{grounding_chunk_index + 1}]"

        print(f"{text_segment} {footnotes_text}")
        prev_index = grounding_support.segment.end_index

    if prev_index < len(text_bytes):
        print(text_bytes[prev_index:].decode(ENCODING))

    print("\n----\n## Grounding Sources\n")

    if grounding_metadata.web_search_queries:
        print(f"\n**Web Search Queries:** {grounding_metadata.web_search_queries}\n")
        if grounding_metadata.search_entry_point:
            print(
                f"\n**Search Entry Point:**\n {grounding_metadata.search_entry_point.rendered_content}\n"
            )
    elif grounding_metadata.retrieval_queries:
        print(f"\n**Retrieval Queries:** {grounding_metadata.retrieval_queries}\n")

    print("### Grounding Chunks\n")

    for index, grounding_chunk in enumerate(
        grounding_metadata.grounding_chunks, start=1
    ):
        context = grounding_chunk.web or grounding_chunk.retrieved_context
        if not context:
            print(f"Skipping Grounding Chunk {grounding_chunk}")
            continue

        print(f"{index}. [{context.title}]({context.uri})\n")
