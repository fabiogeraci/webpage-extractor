from fastapi import FastAPI
from .presentation.api import router


app = FastAPI(title="Webpage Extractor")
app.include_router(router)