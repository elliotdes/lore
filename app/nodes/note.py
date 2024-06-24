from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

from app.state import GraphState

# LLM
llm = ChatOllama(model="llama3", format="json")

prompt = PromptTemplate(
    template="""You are an atomic note generator who creates atomic notes based on the answer to that question. \n 
    Here is the question: {question} \n
    Here is the answer to the question: {answer} \n
    Use three sentences maximum and keep the body of the note concise. \n
    Make the title one sentence long and keep it concise. \n
    You may include up to 3 tags that summarise what is included in the note. You do not need to include tags. \n
    Provide the note as a JSON object with three keys; 'title', 'body', 'tags' and no premable or explanation.""",
    input_variables=["question", "answer"],
)

note_generator = prompt | llm | JsonOutputParser()


def call_note_generator(state: GraphState):
    """
    Create an atomic note based on a user's question and answer.
    """

    question = state["question"]
    answer = state["answer"]

    response = note_generator.invoke({"question": question, "answer": answer})
    print(response)
    return {"note": response}
