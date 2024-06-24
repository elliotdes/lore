from langgraph.graph import END, StateGraph

from app.nodes.generate import call_generate
from app.nodes.grade import call_grader
from app.nodes.note import call_note_generator
from app.nodes.retrieve import call_retriever
from app.state import GraphState


def get_user_input(state: GraphState) -> bool:
    print(state["answer"])
    no_context = state["no_context"]

    if no_context:
        user_input = input("Do you want to generate a note? y/[n]: ").strip().lower()

        if user_input == "y":
            return True
        elif user_input == "n" or user_input == "":
            return False
        else:
            print("Invalid input")
            return get_user_input(state)
    else:
        return False


# Define a new graph
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("retrieve", call_retriever)
workflow.add_node("grade_documents", call_grader)
workflow.add_node("answer_question", call_generate)
workflow.add_node("generate_note", call_note_generator)

# Add edges
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_edge("grade_documents", "answer_question")
workflow.add_conditional_edges(
    "answer_question", get_user_input, {False: END, True: "generate_note"}
)
workflow.add_edge("generate_note", END)

# Compile!
app = workflow.compile()

# Run
user_question = input("Ask a question: ")
final_state = app.invoke(input={"question": user_question})

print("\nNotes used:")
for doc in final_state["documents"]:
    print(f"- '{doc.metadata['source']}'")
