from RAG.ingestion.web_loader import GithubDocLoader
from RAG.processing.chunker import DocumentChunker

loader= GithubDocLoader()

doc= loader.load('https://docs.github.com/en/rest/authentication')

chunker= DocumentChunker(min_chunk_size=300)
chunks= chunker.chunk_document(doc, api_name="github")

print(f'Total Chunks: {len(chunks)}')

for i,chunk in enumerate(chunks[:3]):
    print(f'-----------Chunk {i+1}----------')
    print(f'Metadata: {chunk.metadata}')
    print(f"Length of chunk: {len(chunk.page_content)}")
    print(f"Content of Chunk: {chunk.page_content[:300]}")
    print()