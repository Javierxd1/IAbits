import os
from fastapi import APIRouter
from sqlmodel import select
from models.chats import CreateMemoryChat
from db import SessionDep
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

routerChat = APIRouter()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = Chroma(
    persist_directory="./chroma_langchain_db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever()

llm = ChatOpenAI(
    model='gpt-4o',
    temperature=0.3,
    max_tokens = 500,
    api_key=os.getenv('OpenAI_Api_Key')
)

promptTemplate = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content='Eres un experto en hábitos, basado en los aspectos teóricos propuestos por James Clear. No puedes responde nada diferente a hábitos'),
        AIMessage(content='Responde de manera personalizada usando el nombre dado por el usuario'),
        MessagesPlaceholder(variable_name = 'context'),
        MessagesPlaceholder(variable_name='content')
    ])

def ChatConversation(name,prompt,context):
    if context == None:
        context = "Atiende la consulta, es el primer mensaje del usuario"
        message = promptTemplate.invoke({'content':[HumanMessage(content=name),HumanMessage(content=prompt)],
                                         'context': [SystemMessage(content=context)]})
    else:
        message = promptTemplate.invoke({'content':[HumanMessage(content=name),HumanMessage(content=prompt)],
                                         'context': [SystemMessage(content=context)]})
         
    response = llm.invoke(message)
    return response

@routerChat.post('/chat')
async def Conversation(name:str, prompt:str,studentcode:str, session:SessionDep):
    query = select(CreateMemoryChat).where(CreateMemoryChat.studentCode==studentcode).order_by(CreateMemoryChat.id.desc()).limit(3)
    context = session.exec(query).all()

    contextChat = "\n".join(
    [f"user:{data.prompt} \n Asistente:{data.AIanswer}" for data in reversed(context)]
    )
    
    response = ChatConversation(name,prompt,contextChat)

    chat = CreateMemoryChat(
        studentCode = studentcode,
        name = name,
        prompt=prompt,
        AIanswer= response.content
    )
    session.add(chat)
    session.commit()
    return {'Respuesta': response.content}