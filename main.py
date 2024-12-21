from fastapi import FastAPI
from db import create_all_tables
from routers.PDFprocesor import routerPDFprocesor
from routers.Chatting import routerChat



app = FastAPI(lifespan=create_all_tables)


@app.get('/')
async def root():
    return{'message':'Servidor levantado con éxito'}

app.include_router(routerPDFprocesor, tags=['Documents'])
app.include_router(routerChat, tags=['Chats'])
    