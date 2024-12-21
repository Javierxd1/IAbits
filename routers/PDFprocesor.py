from datetime import datetime
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException,status
from apps.processorPDF import ProcesingPDF as ChunkPDF
from apps.vectorizer import Vectorizator
from models.documents import CreateDocument,GetDocument
from db import SessionDep
from sqlmodel import select
import os

routerPDFprocesor = APIRouter()

@routerPDFprocesor.post('/upload_pdf')
async def upload_pdf(session: SessionDep,
                     autors: str,
                     title: str,
                     year: str,
                     description: Optional[str] = None ,
                     file: UploadFile = File(...)
                     ):
    # Verificar si la carpeta "temp" existe
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    # Guardar el archivo temporalmente
    try:
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        document_split, primer_trozo = ChunkPDF(file_path)

        doc = CreateDocument(
            autors= autors,
            year = year,
            title = title,
            uploadDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            description = description
            )
        session.add(doc)
        session.commit()

        vectorStore = Vectorizator(document_split)

        return{
            'Message':'Archivo procesado y vectorizado con éxito',
            'Title': title,
            'Autors': autors,
            'firstChunk': primer_trozo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@routerPDFprocesor.get('/search', response_model= list[GetDocument])
async def Search_Autor(autors: str, session: SessionDep):
    autors = session.exec(
        select(CreateDocument).where(CreateDocument.autors.ilike(f"%{autors}%"))).all()  # Se obtienen todos los resultados que hagan coincidencia.
    
    listAutor = []
    for autor in autors:
        getAutor = GetDocument.model_validate(autor.model_dump())
        listAutor.append(getAutor)

    if autors != None:
        return listAutor[0:3]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Autor no encontrado')