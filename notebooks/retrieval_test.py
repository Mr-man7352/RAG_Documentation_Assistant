from RAG.vectorstore.ingestion import IngestionPipeline

def run_retriever():

    pipeline= IngestionPipeline(
        collection_name='github_issues_api'
    )

    pipeline.ingest_url(
        url='https://docs.github.com/en/rest/issues/issues',
        api_name='github'
    )

    retriever= pipeline.vector_store.as_retriever(
        search_kwargs={'k':5}
    )

    query='How do I create an issue using the GitHub REST API?'

    print(f'User Query: {query}')

    result= retriever.invoke(query)

    print(f"Retrieved {len(result)} Documents!")

    for i, doc in enumerate(result, start=1):
        print(f'----Results {i}------')
        print(f'Chunk Length: {len(doc.page_content)}')
        print(doc.page_content[:300])


if __name__=='__main__':
    run_retriever()


