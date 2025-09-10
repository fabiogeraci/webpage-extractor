from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..application.extract_usecase import ExtractUseCase
from ..infrastructure.storage.filesystem_storage import FilesystemStorage
from ..config import settings


router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")

# Simple factory to resolve destinations list without coupling
def _storage(data_path: str = None) -> FilesystemStorage:
    return FilesystemStorage(base_dir=data_path)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": None
    })


@router.post("/extract", response_class=HTMLResponse)
async def extract(request: Request,
                        url: str = Form(...),
                        new_destination: str = Form(""),
                        usecase: ExtractUseCase = Depends()):
    # Use the new_destination as the full path, or default to exports folder
    dest_path = new_destination or "exports"
    
    # Create storage with the specified path
    storage = _storage(dest_path)
    
    # Update the usecase with the new storage
    usecase.storage = storage
    
    result = await usecase.execute(url=url, destination_name="")
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": result
    })