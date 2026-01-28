from markdownify import markdownify
from langchain.text_splitter import MarkdownHeaderTextSplitter

class DocumentChunker:
    def __init__(self, min_chunk_size : int =300):
        self.min_chunk_size = min_chunk_size

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