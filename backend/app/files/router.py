from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.files import service
from app.files.schemas import FileOut, FolderCreate, FolderOut

router = APIRouter()

@router.post("/", response_model=FileOut)
def upload_file(folder_path: str | None = None, upload: UploadFile = FastAPIFile(...), db: Session = Depends(get_db)):
    return service.save_upload(db=db, folder_path=folder_path, upload=upload)

@router.get("/")
def list_files(db: Session = Depends(get_db)):
    return service.list_files(db)

@router.post('/folder', status_code=status.HTTP_201_CREATED, response_model=FolderOut)
def create_folder(body: FolderCreate, db: Session = Depends(get_db)):
    result = service.create_folder(db, body.name)
    if result is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="já existe uma pasta com esse nome")
    return result