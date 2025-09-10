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
async def index(request: Request, data_path: str = None):
    storage = _storage(data_path)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "destinations": storage.list_destinations(), 
        "result": None,
        "current_data_path": data_path or settings.default_data_dir,
        "default_data_path": settings.default_data_dir
    })


@router.post("/extract", response_class=HTMLResponse)
async def extract(request: Request,
                        url: str = Form(...),
                        destination: str = Form(""),
                        new_destination: str = Form(""),
                        data_path: str = Form(""),
                        usecase: ExtractUseCase = Depends()):
    dest_name = new_destination or destination or "exports"
    selected_data_path = data_path or settings.default_data_dir
    
    # Create storage with selected data path
    storage = _storage(selected_data_path)
    
    # Update the usecase with the new storage
    usecase.storage = storage
    
    result = await usecase.execute(url=url, destination_name=dest_name)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "destinations": storage.list_destinations(), 
        "result": result,
        "current_data_path": selected_data_path,
        "default_data_path": settings.default_data_dir
    })