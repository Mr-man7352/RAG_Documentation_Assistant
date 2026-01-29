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

    generator= RAGGenerator(pipeline.vector_store)

    question = 'How do I create an issue using GitHub REST API?'

    result= generator.ask(question)