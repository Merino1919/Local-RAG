import os
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_core.tools import tool

# Importamos tus utils
from app.utils.embeddings import get_embeddings_model
from app.utils.parsers import select_loader

class RAGEngine:
    def __init__(self, model_name="qwen3:8b", base_url="http://172.31.233.250:11434/"):
        self.embeddings = get_embeddings_model()
        self.llm = ChatOllama(model=model_name, base_url=base_url, temperature=0)
        
        self.persist_directory = "./app/data/chroma_db"
        self.vector_store = None

    def ingest_document(self, file_path: str):
        loader = select_loader(file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            add_start_index=True
        )
        splits = text_splitter.split_documents(docs)

        self.vector_store = Chroma.from_documents(
            collection_name="rag_docs",
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return f"Document '{os.path.basename(file_path)}' correctly indexed."

    def get_response(self, query: str):
        if not self.vector_store:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

        system_prompt = (
            "You are an expert analyst working over sensitive documents. "
            "Use the provided context to answer the question. If the answer is not "
            "available in the context, state it. Do not invent data."
            "\n\n"
        )
 
        @tool
        def search_documents(query:str): 
            docs = self.vector_store.similarity_search(query, k=5)
            context = "\n\n".join([d.page_content for d in docs])
            print(f"DEBUG - Retrieved context: {context}")
            return context
        
        tools = [search_documents]


        agent = create_agent(self.llm, tools, system_prompt= system_prompt)
        
        result = ""
        for event in agent.stream({"messages": [{"role": "user", "content": query}]}, stream_mode="values"):
            last_msg = event["messages"][-1]
            last_msg.pretty_print()
            final_response = last_msg.content
        
        return final_response 
    
        