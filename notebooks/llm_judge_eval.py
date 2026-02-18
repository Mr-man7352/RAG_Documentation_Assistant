import os
from langchain_groq import ChatGroq


judge_llm= ChatGroq(
    api_key= os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=20
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


def hallucination_score(context, answer, runs=3):

    score=[]

    for _ in range(runs):

        prompt = f"""
            You are evaluating a RAG system.

            Context:
            {context}

            Answer:
            {answer}

            Check if the answer includes factual claims that are NOT supported by the context.

            Ignore:
            - rephrasing
            - formatting
            - summarization
            - minor wording differences

            Only mark hallucination if the answer introduces NEW factual information not present in context.

            Reply ONLY with YES or NO.
            """

        response = judge_llm.invoke(prompt).content.strip().lower()

        if "yes" in response:
            score.append(1)  # hallucination is present
        else:
            score.append(0)   # no hallucination

    return sum(score)/len(score)        
