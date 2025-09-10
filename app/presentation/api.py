from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from urllib.parse import urlparse
from ..application.extract_usecase import ExtractUseCase
from ..infrastructure.storage.filesystem_storage import FilesystemStorage
from ..infrastructure.http.httpx_client import HttpxClient
from ..infrastructure.extraction.accordion_content_extractor import AccordionContentExtractor
from ..infrastructure.extraction.image_extractor import ImageExtractor
from ..config import settings


router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": None
    })


@router.post("/extract", response_class=HTMLResponse)
async def extract(request: Request,
                        url: str = Form(...),
                        new_destination: str = Form("")):
    try:
        # Use the new_destination as the full path, or default to exports folder
        dest_path = new_destination or "exports"
        
        print(f"Extracting from URL: {url}")
        print(f"Destination path: {dest_path}")
        
        # Create all dependencies manually
        http = HttpxClient()
        content_ext = AccordionContentExtractor()
        image_ext = ImageExtractor()
        
        # Create storage with the user's destination path as base_dir
        storage = FilesystemStorage(base_dir=dest_path)
        
        # Create use case with all dependencies
        usecase = ExtractUseCase(http, content_ext, image_ext, storage)
        
        # Use empty destination_name to save directly in base_dir
        result = await usecase.execute(url=url, destination_name="")
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": result
        })
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "result": None,
            "error": str(e)
        })