from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.files import service
from app.files.schemas import FileOut

router = APIRouter()

@router.post("/", response_model=FileOut)
def upload_file(upload: UploadFile = FastAPIFile(...), db: Session = Depends(get_db)):
    return service.save_upload(db, upload)