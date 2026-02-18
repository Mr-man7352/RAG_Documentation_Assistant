
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
import os

class RAGGenerator:

    """
    Generation Layer
    
    """

    def __init__(self, vector_store, groq_api_key=None):

        

        self.llm= ChatGroq(
            api_key=groq_api_key or os.getenv('GROQ_API_KEY'),
            #model_name='llama-3.3-70b-versatile',
            model_name='llama-3.3-8b-versatile',
            temperature=0.1,
            max_tokens=1500
        )

        self.retriever= vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={ 'k' : 12,
                           'fetch_k':20,
                           'lambda_mult' : 0.7}
        )

        self.rag_chain = self.build_chain()

    def format_docs(self, docs):

        "Merges all the retrieved docs into a single document"

        return "\n\n".join(doc.page_content for doc in docs)    
        

    def build_chain(self):

        prompt= ChatPromptTemplate.from_template(
           
            """You are an expert API documentation assistant specializing in GitHub's REST API.

            Use the following documentation context to answer the user's question accurately and helpfully.

            Documentation Context:
            {context}

            Question: {question}

            Instructions:
            - Answer based ONLY on the provided documentation above
            - Be specific and include exact endpoint paths, HTTP methods, and parameter names
            - Include code examples from the documentation when available
            - If the documentation shows request/response examples, include them
            - Format your response clearly with proper structure
            - If you cannot find the answer in the documentation, say so explicitly
            - For API endpoints, always mention:
            * HTTP method (GET, POST, etc.)
            * Endpoint path
            * Required parameters
            * Authentication requirements (if mentioned)

            Answer:"""

        )
        

        rag_chain=(

            {
                "context" : self.retriever | self.format_docs,
                "question" : RunnablePassthrough()
            }

            | prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain
    
    def generate(self,question):
        return self.rag_chain.invoke(question)








