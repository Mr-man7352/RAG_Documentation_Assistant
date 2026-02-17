from RAG.vectorstore.ingestion import IngestionPipeline
from RAG.generation.rag_chain import RAGGenerator
from RAG.notebooks.llm_judge_eval import groundedness_score, relevance_score, completeness_score
import os


pipeline= IngestionPipeline(
    collection_name='github_issues_api_gen'
)

pipeline.ingest_url(
        url='https://docs.github.com/en/rest/issues/issues',
        api_name='github'
    )


generator= RAGGenerator(
                        vector_store= pipeline.vector_store,
                        groq_api_key=os.getenv("GROQ_API_KEY")
                        )

retriever= pipeline.vector_store.as_retriever(
        search_kwargs={
                        'k':12, 
                      }

    )


#Test Questions

questions = [
    "How do I create an issue using GitHub REST API?",
    "How do I update an issue?",
    "How do I lock an issue?",
    "How do I get an issue?"
]

grounded_scores = []

relevance_scores = []

complete_scores = []

for q in questions:

    print("Question: ",q)

    docs = retriever.invoke(q)

    context = "\n".join([d.page_content for d in docs])

    answer = generator.generate(q)

    print("Answer: ", answer[:300])

    gs = groundedness_score(q, context, answer)

    rs = relevance_score(q, answer)

    cs= completeness_score(q, answer)

    grounded_scores.append(gs)

    relevance_scores.append(rs)
    
    complete_scores.append(cs)
     
    print("Groundedness: ", gs)
    print("Relevance: ", rs) 
    print("Completeness : ", cs) 



print("\n==============================")
print("FINAL SCORES")
print("Avg Groundedness:", sum(grounded_scores)/len(grounded_scores))
print("Avg Relevance:", sum(relevance_scores)/len(relevance_scores))
print("Avg Completeness:", sum(complete_scores)/len(complete_scores))





