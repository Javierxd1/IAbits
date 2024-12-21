from sqlmodel import SQLModel, Field


class Documents(SQLModel):
    autors: str
    title: str
    year: str
    uploadDate: str
    description: str = Field(default=None, nullable=True)

class CreateDocument(Documents, table = True):
    id : int = Field(default=None, primary_key=True)

class GetDocument(Documents):
    pass