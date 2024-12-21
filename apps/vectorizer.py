from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
def Vectorizator(documents = None):
#Se inicia la base de datos en Chroma
    Chroma(
        collection_name="Habits_articles",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )
    vector_store = Chroma.from_documents(
        documents= documents,
        embedding= embeddings
    )
    return vector_store
