from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from RAG.ingestion.web_loader import GithubDocLoader
from RAG.processing.chunker import DocumentChunker

class IngestionPipeline:
    def __init__(self, collection_name : str ="api_docs"):

        #Initializing Embedding Model
        self.embeddings= HuggingFaceEmbeddings(
            model_name='all-MiniLM-L6-v2'
        )

        #Initializaing Qdrant Client (in-memory)
        self.client = QdrantClient(":memory:")

        #Creating Vector Store
        self.vector_store= QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embeddings
        )

        print('Pipeline Ready!')

    def ingest_url(self, url : str, api_name: str):

        """
        This function will -
        Load -> Chunks -> Embed and Index

        """    
        print("Ingesting {url}")
        # Loading
        loader= GithubDocLoader()
        docs= loader.load(url)

        #Chunking
        chunker= DocumentChunker()
        chunks= chunker.chunk_document(docs, api_name)

        #Embedding and Indexing
        self.vector_store.add_documents(chunks)

        print(f"Indexed {len(chunks)} chunks!")

        return chunks