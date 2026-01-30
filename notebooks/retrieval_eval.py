from RAG.vectorstore.ingestion import IngestionPipeline

def build_test_set():
    """
    Ground-truth style test questions
    expected_keyword = text that MUST appear in correct chunk
    """

    return [
        {
            "question" : "How do I create an issue using Github REST API?",
            "expected_keyword" : "Create an issue"
        },

        {
            "question" : "How do I lock an issue?",
            "expected_keyword" : "Lock an issue"
        },

        {
            "question" : "How do I update an issue?",
            "expected_keyword" : "Update an issue"
        },

        {
            "question" : "How do I get an issue?",
            "expected_keyword" : "Get an issue"
        }

    ]

def evaluate_hit_at_k(retriever, test_cases, k=8):

    hits=0

    for case in test_cases:

        question= case['question']
        expected= case['expected_keyword'].lower()

        print(f"QUESTION: {question}")

        docs= retriever.invoke(question)

        found= False

        for i, doc in enumerate(docs[:k]):

            if expected in (doc.page_content.lower()):
                found=True
                print(f'Expected Keyword found after {i+1} results')
                break
                
        if found:
            hits+=1

        else:
            print("Not found in top-K results!")   

    score= hits / len(test_cases)   

    print(f"Hit@{k}: {score:.2%}")   

def run_eval():
    
    pipeline = IngestionPipeline(
        collection_name="github_issues_api"
    )
    
    pipeline.ingest_url(
        url="https://docs.github.com/en/rest/issues/issues",
        api_name="github"
    )
    
    retriever = pipeline.vector_store.as_retriever(
        search_kwargs={"k": 8}
    )
    
    test_cases = build_test_set()
    
    evaluate_hit_at_k(retriever, test_cases, k=8)


if __name__ == "__main__":
    run_eval()       
