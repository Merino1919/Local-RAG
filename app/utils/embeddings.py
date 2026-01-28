from langchain_ollama import OllamaEmbeddings

def get_embeddings_model():
    # Usamos nomic-embed-text por ser eficiente en la Tesla T4
    return OllamaEmbeddings(
        model="qwen3-embedding:4b",
        base_url="http://172.31.233.250:11434/"
    )
    
    
# embeddinggemma:300m 
# nomic-embed-text:latest
# nomic-embed-text-v2-moe:latest 