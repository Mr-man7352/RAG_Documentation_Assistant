from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAGGenerator:

    """
    Generation Layer
    
    """

    def __init__(self, vector_store):

        model_name='google/flan-t5-small'

        tokenizer= AutoTokenizer.from_pretrained(model_name)
        model= AutoModelForSeq2SeqLM.from_pretrained(model_name)

        hf_pipeline= pipeline(
            'text-generation',
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512
        )

        self.llm= HuggingFacePipeline(pipeline=hf_pipeline)

        self.retriever= vector_store.as_retriever(
            search_kwargs={ 'k' : 6}
        )

        self.rag_chain = self.build_chain()

    def format_docs(self, docs):

        "Merges all the retrieved docs into a single document"

        return "\n\n".join(doc.page_content for doc in docs)    

    def build_chain(self):

        prompt= ChatPromptTemplate.from_template(
            """
            You are an expert API documentation assistant.

            Answer ONLY using the provided documentation context.

            Context:
            {context}

            Question:
            {question}

            Rules:
            - Be precise
            - Include endpoint names when possible
            - Include code snippets if present
            - If answer not found — say so clearly

            """
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








