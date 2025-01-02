from enum import Enum
from operator import attrgetter
from typing import Optional

from fastapi import FastAPI, Query, Depends
from fastapi.responses import FileResponse
from fastapi_utilities import repeat_every
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from random import shuffle
import lib

class SortMethod(str, Enum):
    random = "random"
    az = "az"
    za = "za"

class ListBooksQuery(BaseModel):
    sort: Optional[SortMethod] = Field(Query(default=SortMethod.random))

@asynccontextmanager
async def lifespan(app: FastAPI):
    lib.parse_library()
    yield

@repeat_every(seconds=60*60)
async def reparse_library():
    lib.parse_library()


app = FastAPI(lifespan=lifespan)

@app.get("/list-books")
def list_books(sort: SortMethod = SortMethod.random):
    books = lib.list_books()

    if sort is SortMethod.random:
        shuffle(books)
    elif sort is SortMethod.az:
        books.sort(key=attrgetter("title"), reverse=False)
    elif sort is SortMethod.za:
        books.sort(key=attrgetter("title"), reverse=True)

    return books


@app.get("/download/{id}")
def download(id: str):
    path, filename = lib.download_book(id)

    return FileResponse(
        path=path, media_type="application/octet-stream", filename=filename
    )
