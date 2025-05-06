from transformers import pipeline

# Load the question answering pipeline with a Hugging Face model
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Predefined context containing educational content on various subjects
context = """
Science is the systematic enterprise that builds and organizes knowledge through testable explanations and predictions about the universe.
Mathematics is the study of topics such as quantity, structure, space, and change.
History examines and interprets past events as they relate to humans.
Programming is the process of designing and building an executable computer program to accomplish a specific computing task.
"""

def get_answer(question):
    try:
        result = qa_pipeline(question=question, context=context)
        return result['answer']
    except Exception as e:
        return f"Sorry, I couldn't process the question due to an error: {str(e)}"
