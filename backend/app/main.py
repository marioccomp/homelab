from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.files.router import router as files_router

app = FastAPI(title="Homelab API")

app.include_router(auth_router, prefix='/auth', tags=["auth"])
app.include_router(files_router, prefix='/files', tags=["files"])

@app.get("/health")
def health():
    return {"status": "ok"}


