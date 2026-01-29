from RAG.vectorstore.ingestion import IngestionPipeline

if __name__=="__main__":
    pipeline= IngestionPipeline(
        collection_name='github_issues_api'
    )

    chunks= pipeline.ingest_url(
        url='https://docs.github.com/en/rest/issues/issues',
        api_name='github'
    )

    print(f'Total Chunks Ingested: {len(chunks)}')