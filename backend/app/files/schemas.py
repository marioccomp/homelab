from datetime import datetime
from pydantic import BaseModel

class FileOut(BaseModel):
    id: int
    original_filename: str
    content_type: str
    size_bytes: int
    created_at: datetime

    class Config:
        from_attributes = True

class FolderCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True

class FolderOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
