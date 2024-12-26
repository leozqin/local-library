from fastapi import FastAPI
from fastapi.responses import FileResponse
import lib

app = FastAPI()


@app.get("/list-books")
def list_books():
    return lib.list_books()


@app.get("/download/{id}")
def download(id: str):
    path, filename = lib.download_book(id)

    return FileResponse(
        path=path, media_type="application/octet-stream", filename=filename
    )
