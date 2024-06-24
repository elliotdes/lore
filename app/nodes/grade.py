from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

from app.state import GraphState

# LLM
llm = ChatOllama(model="llama3", format="json", temperature=0)

prompt = PromptTemplate(
    template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
    Here is the retrieved document: \n\n {document} \n\n
    Here is the user question: {question} \n
    If the document contains keywords related to the user question, grade it as relevant. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
    Provide the binary score as a JSON with a single key 'score' and no premable or explanation.""",
    input_variables=["question", "document"],
)

retrieval_grader = prompt | llm | JsonOutputParser()


def call_grader(state: GraphState):
    """
    Determines whether the retrieved documents are relevant to the question.
    """

    question = state["question"]
    documents = state["documents"]

    # Score each doc
    filtered_docs = []
    no_context = False
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.get("score", "no")
        if grade == "yes":
            filtered_docs.append(d)

    if not filtered_docs:
        no_context = True
    return {"documents": filtered_docs, "question": question, "no_context": no_context}
