import os
from langchain_groq import ChatGroq


judge_llm= ChatGroq(
    api_key= os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=200
)


def groundedness_score(question, context, answer):

    prompt= f"""
        You are aevaluating a RAG system.

        Question:{question}

        Context :
        {context}

        Answer :
        {answer}

        Is this answer fully supported by the context? 
        Reply only in YES or NO

    """

    response= judge_llm.invoke(prompt).content.strip().lower()

    if "yes" in response:
        return 1
    else:
        return 0
    



def relevance_score(question, answer):

    prompt= f"""

    Question : {question}

    Answer :
    {answer}

    Rate the relevance of the answer with respect to question on a scale of 1 to 5.
    Only return number.

    """

    response = judge_llm.invoke(prompt).content.strip()

    return int(response)


def completeness_score(question, answer):

    prompt = f"""

    Question: {question}

    Answer : {answer}

    Does this answer fully and completely address the question?
    Only answer as yes or no.

    """

    llm_response= judge_llm.invoke(prompt).content.lower()

    if "yes" in llm_response:
        return 1
    else:
        return 0


def hallucination_score(context, answer):

    prompt = f"""
You are evaluating a RAG system.

Context:
{context}

Answer:
{answer}

Does the answer contain any information that is NOT present in the context?
Reply ONLY with YES or NO.
"""

    response = judge_llm.invoke(prompt).content.strip().lower()

    if "yes" in response:
        return 1   # hallucination present
    else:
        return 0   # no hallucination
