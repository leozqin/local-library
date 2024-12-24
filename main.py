from fastapi import FastAPI
import lib

app = FastAPI()

@app.get("/list-books")
def list_books():
    return lib.list_books()