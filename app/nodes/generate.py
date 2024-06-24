from langchain import hub
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from app.state import GraphState

llm = ChatOllama(model="llama3")
context_prompt = hub.pull("rlm/rag-prompt")

no_context_prompt = PromptTemplate(
    template="""You are an assistant for question-answering tasks. \n 
    If you don't know the answer, just say that you don't know. \n
    Use three sentences maximum and keep the answer concise. \n
    Here is the user question: {question} \n""",
    input_variables=["question"],
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def call_generate(state: GraphState):
    question = state["question"]
    documents = state["documents"]
    no_context = state["no_context"]

    prompt = no_context_prompt if no_context else context_prompt

    rag_chain = prompt | llm | StrOutputParser()
    response = rag_chain.invoke(
        {"question": question, "context": format_docs(documents)}
    )
    return {
        "answer": response,
        "documents": documents,
        "question": question,
    }
