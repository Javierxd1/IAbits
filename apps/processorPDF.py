from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def ProcesingPDF (file_path:str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 30
    )
    document_split =  text_spliter.split_documents(pages)

    #Validación
    if len(document_split) > 0:
        first_chunk = document_split[0].page_content
    else:
        first_chunk = 'El documento no posee texto procesable'
        
    return document_split,first_chunk