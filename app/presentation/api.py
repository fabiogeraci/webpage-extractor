from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..application.extract_usecase import ExtractUseCase
from ..infrastructure.storage.filesystem_storage import FilesystemStorage


router = APIRouter()
templates = Jinja2Templates(directory="app/presentation/templates")

# Simple factory to resolve destinations list without coupling
def _storage() -> FilesystemStorage:
    return FilesystemStorage()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    storage = _storage()
    return templates.TemplateResponse("index.html", {"request": request, "destinations": storage.list_destinations(), "result": None})


@router.post("/extract", response_class=HTMLResponse)
async def extract(request: Request,
                        url: str = Form(...),
                        destination: str = Form(""),
                        new_destination: str = Form("") ,
                        usecase: ExtractUseCase = Depends()):
    dest_name = new_destination or destination or "exports"
    result = await usecase.execute(url=url, destination_name=dest_name)
    storage = _storage()
    return templates.TemplateResponse("index.html", {"request": request, "destinations": storage.list_destinations(), "result": result})