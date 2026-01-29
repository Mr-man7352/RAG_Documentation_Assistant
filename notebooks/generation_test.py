from RAG.vectorstore.ingestion import IngestionPipeline
from RAG.generation.rag_chain import RAGGenerator

def run_generation():

    pipeline = IngestionPipeline(
        collection_name='github_issues_api_gen'
    )

    pipeline.ingest_url(
        url='https://docs.github.com/en/rest/issues/issues',
        api_name='github'
    )

    generator= RAGGenerator(vector_store= pipeline.vector_store)

    question = 'How do I create an issue using GitHub REST API?'

    print(f"---QUESTION----{question}")

    answer= generator.generate(question)

    print(f"-----ANSWER-------{answer}")



if __name__ == "__main__":
    run_generation()