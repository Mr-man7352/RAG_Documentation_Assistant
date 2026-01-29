from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

class RAGGenerator:

    """
    Generation Layer
    
    """

    def __init__(self, vector_store):

        model_name='google/flan-t5-base'

        tokenizer= AutoTokenizer.from_pretrained(model_name)
        model=AutoModelForCausalLM.from_pretrained(model_name)

        hf_pipeline= pipeline(
            'text2text-generation',
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512
        )

        self.llm= HuggingFacePipeline(pipeline=hf_pipeline)

        self.retriever= vector_store.as_retriever(
            search_kwargs={ 'k' : 6}
        )

        self.build_chain()

    def build_chain(self):

        system_prompt = """You are an expert GitHub REST API assistant.

        Answer ONLY using the provided documentation context.

        Rules:
        - If answer not found → say "Not found in documentation"
        - Prefer endpoint + method names
        - Include code examples if present
        - Be precise and technical

        Documentation Context:
        {context}
        """    

        prompt= ChatPromptTemplate([
            ('system',system_prompt),
            ('user',{input})
        ])

        qa_chain= create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt
        )

        self.rag_chain= create_retrieval_chain(
            retriever= self.retriever,
            combine_docs_chain= qa_chain
        )

    def ask(self, question):

        result= self.rag_chain.invoke({'input':question})

        return result