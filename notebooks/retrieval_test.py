from RAG.vectorstore.ingestion import IngestionPipeline
from qdrant_client.models import Filter, FieldCondition, MatchValue


def run_retriever():

    pipeline= IngestionPipeline(
        collection_name='github_issues_api'
    )

    pipeline.ingest_url(
        url='https://docs.github.com/en/rest/issues/issues',
        api_name='github'
    )


    retriever= pipeline.vector_store.as_retriever(
        search_kwargs={
                        'k':12, 
                      }

    )

    query='How do I create an issue using the GitHub REST API?'

    print(f'User Query: {query}')

    result= retriever.invoke(query)

    final_result= re_rank_results(result)

    print(f"Retrieved {len(final_result)} Documents!")

    for i, doc in enumerate(final_result, start=1):
        print(f'----Results {i}------')
        print(f'Chunk Length: {len(doc.page_content)}')
        print(doc.page_content[:300])
        print(doc.metadata)

def re_rank_results(docs):

    keywords=['create','post','add']

    def score(docs):
        text = docs.page_content.lower()

        return sum(kw in text for kw in keywords) 

    return sorted(docs, key=score, reverse=True)       


if __name__=='__main__':
    run_retriever()


