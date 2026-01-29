from markdownify import markdownify
from langchain.text_splitter import MarkdownHeaderTextSplitter

class DocumentChunker:
    def __init__(self, min_chunk_size : int =300, max_chunk_size : int = 1500):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size

        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ('##','h2'),
                ('###','h3')
            ],
            strip_headers=False
        )

    def chunk_document(self, doc_data: dict, api_name: str) -> list:
        """
        Convert a loaded HTML document into semantic chunk
        
        """
        #Converting from HTML to Markdown
        markdown_content= markdownify(str(doc_data['html']))

        # Chunking the markdown data (Header-based)
        chunks= self.markdown_splitter.split_text(markdown_content)

        #Merging small chunks

        chunks= self.merge_small_chunks(chunks)

        #Attach Metadata

        for chunk in chunks:
            chunk.metadata.update(
                {
                    "api_name" : api_name,
                    "source_url" : doc_data['source'],
                    "page_title" : doc_data['title'],
                    "doc_type" : doc_data['doc_type'],
                    "contains_code" : "```" in chunk.page_content
                }
            )
        return chunks
    
    def merge_small_chunks(self, chunks):

        """
        Merges small adjacent chunks

        """
        merged=[]
        buffer=None

        for chunk in chunks:
            if len(chunk.page_content) < self.min_chunk_size:

                if buffer is None:
                    buffer= chunk

                else:
                    if len(buffer.page_content) + len(chunk.page_content) <= self.max_chunk_size:
                        buffer.page_content += "\n\n" + chunk.page_content
                    else:
                        merged.append(buffer)
                        buffer=None
                        buffer = chunk    

            else:
                if buffer:
                    merged.append(buffer)
                    buffer=None           
                merged.append(chunk)

        if buffer:
            merged.append(buffer)

        return merged    

