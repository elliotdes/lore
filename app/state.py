from typing import TypedDict

from langchain_core.documents import Document


class GraphState(TypedDict):
    question: str
    answer: str
    no_context: bool  # if no context was provided to the LLM
    documents: list[Document]
    note: dict  # Obsdidian note
