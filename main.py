from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi_utilities import repeat_every
from contextlib import asynccontextmanager
from random import shuffle
import lib

@asynccontextmanager
async def lifespan(app: FastAPI):
    lib.parse_library()
    yield

@repeat_every(seconds=60*60)
async def reparse_library():
    lib.parse_library()


app = FastAPI(lifespan=lifespan)

@app.get("/list-books")
def list_books():
    books = lib.list_books()
    shuffle(books)
    
    return books


@app.get("/download/{id}")
def download(id: str):
    path, filename = lib.download_book(id)

    return FileResponse(
        path=path, media_type="application/octet-stream", filename=filename
    )
