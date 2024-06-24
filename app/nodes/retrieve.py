import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import ObsidianLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.state import GraphState

obsidian_vault = os.getenv("OBSIDIAN_VAULT")
if not obsidian_vault:
    raise ValueError("Please set OBSIDIAN_VAULT env variable.")

loader = ObsidianLoader(path=obsidian_vault)
text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=0
)
notes = loader.load_and_split(text_splitter=text_splitter)


vectorstore = Chroma.from_documents(
    documents=notes, embedding=OllamaEmbeddings(model="nomic-embed-text")
)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})


def call_retriever(state: GraphState):
    """
    Retrieve relevant notes from Obsidian.
    """
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents}
