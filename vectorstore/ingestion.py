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

        self.collection_name= collection_name

        #Creating Vector Store
        self.vector_store=None

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

        print(f"Length of chunks: {len(chunks)}")

        for i, chunk in enumerate(chunks):
            print(f"-----------Printing Chunk{i}--------")
            print(f"Chunk Length: {len(chunk.page_content)}")


        #Embedding and Indexing

        if self.vector_store is None:
            self.vector_store= QdrantVectorStore.from_documents(
                documents=chunks,
                collection_name=self.collection_name,
                embedding=self.embeddings,
                location=":memory:"
            )
        else:
            self.vector_store.add_documents(chunks)

        print(f"Indexed {len(chunks)} chunks!")

        return chunks