from sqlmodel import SQLModel, Field
from datetime import datetime

class MemoryChat(SQLModel):
    studentCode: str
    name: str
    prompt: str
    AIanswer :str

class CreateMemoryChat(MemoryChat, table = True):
    id: int = Field(default=None, primary_key=True)
    