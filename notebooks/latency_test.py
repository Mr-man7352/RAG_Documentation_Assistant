import time
from RAG.generation.rag_chain import RAGGenerator
from RAG.vectorstore.ingestion import IngestionPipeline

def run_latency_test():

    pipeline= IngestionPipeline(
        collection_name="github_issues_api"
    )

    pipeline.ingest_url(
        url="https://docs.github.com/en/rest/issues/issues",
        api_name="github"
    )

    generator = RAGGenerator(vector_store= pipeline.vector_store)

    questions=[
            "How do I create an issue using GitHub REST API?",
            "How do I lock an issue?",
            "How do I update an issue?",
            "How do I get an issue?"
    ]

    latencies= []

    for q in questions:
        

        start= time.time()

        answer= generator.generate(q)

        end= time.time()

        latency= end-start

        latencies.append(latency)

    print(latencies)    

    avg_latency= sum(latencies)/  len(latencies)   

    print("Average Latency:", round(avg_latency, 3), "seconds")


if __name__=="__main__":
    run_latency_test()