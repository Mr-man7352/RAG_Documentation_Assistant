from markdownify import markdownify
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentChunker:
    def __init__(self, min_chunk_size : int =400, max_chunk_size : int = 2000, target_chunk_size : int = 1200):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.target_chunk_size = target_chunk_size

        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ('#','h1'),
                ('##','h2'),
                ('###','h3')
            ],
            strip_headers=False
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size= target_chunk_size,
            chunk_overlap=100,
            separators=["\n### ",
                "\n## ",
                "\n```",     # split before code blocks
                "\n\n",
                "\n",
                ". ",
                " ",
                ""]
        )

    def chunk_document(self, doc_data: dict, api_name: str) -> list:
        """
        Convert a loaded HTML document into semantic chunk
        
        """
        #Converting from HTML to Markdown
        markdown_content= markdownify(str(doc_data['html']))
        print("Content before chunking: ",markdown_content[:1200])

        # Chunking the markdown data (Header-based)
        chunks= self.markdown_splitter.split_text(markdown_content)
        print(f'Chunks after Markdown Splitter: {len(chunks)}')

        # Enforcing Max Size Restrictions on each chunk
        chunks= self.enforce_max_size(chunks)
        print(f'Chunks after Enforcing Max Size Restrictions: {len(chunks)}')

        #Merging small chunks
        chunks= self.merge_small_chunks(chunks)
        print(f'Chunks after Merging small chunks: {len(chunks)}')

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
    
    def enforce_max_size(self, chunks):

        processed=[]

        for chunk in chunks:
            if(len(chunk.page_content)) <= self.max_chunk_size:
                processed.append(chunk)
                continue

            print('Oversized Chunk Detected! Splitting it!')

            sub_text= self.text_splitter.split_text(chunk.page_content)

            for i, text in enumerate(sub_text):
                processed.append(
                    Document(
                        page_content = text,
                        metadata = {
                            **chunk.metadata,
                            'split_from_bigger_chunk' : True,
                            'split_part' : i+1
                        }

                    )
                )
            print(f'Created {len(sub_text)} chunks from the bigger one')

        return processed    
