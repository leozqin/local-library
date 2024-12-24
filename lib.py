from pathlib import Path
from typing import List, Self
from pydantic import BaseModel, computed_field
from hashlib import md5
from os import environ
from glob import glob

from PIL.Image import open as open_img, Image
from ebooklib.epub import read_epub, EpubBook, IMAGE_MEDIA_TYPES, EpubCover
from ebooklib import ITEM_COVER
from tinydb import TinyDB, Query

DATA_DIR = Path(environ.get("DATA_DIR", Path(__file__).parent.joinpath("data")))
DB_DIR = Path(DATA_DIR, "db")
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = Path(DB_DIR, "db.json")

PUBLIC_DIR = Path(Path(__file__).parent.joinpath("web/public"))
COVERS_DIR = Path(PUBLIC_DIR, "covers")

ORIGINALS_DIR = Path(COVERS_DIR, "originals")
ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)

SM_DIR = Path(COVERS_DIR, "sm")
SM_DIR.mkdir(parents=True, exist_ok=True)
MD_DIR = Path(COVERS_DIR, "md")
MD_DIR.mkdir(parents=True, exist_ok=True)
LG_DIR = Path(COVERS_DIR, "lg")
LG_DIR.mkdir(parents=True, exist_ok=True)

SM = 200, 200
MD = 400, 400
LG = 600, 600

db = TinyDB(str(DB_PATH.resolve()))


class BookNotFoundException(Exception):
    pass


class Book(BaseModel):
    title: str
    creators: List[str]
    local_path: str
    language: str = "en"

    @computed_field
    @property
    def id(self) -> str:
        return md5(self.local_path.encode()).hexdigest()

    def to_record(self) -> None:
        rec = {"id": self.id, "data": self.model_dump()}
        query = Query()
        db.upsert(rec, query.id == self.id)

    @classmethod
    def from_record(cls, id: str) -> Self:
        query = Query()
        try:
            record = db.search(query.id == id)[0]
            data = record.get("data")
        except (IndexError, KeyError) as e:
            raise BookNotFoundException from e

        return Book(**data)


def make_book(path: Path) -> Book:
    book = read_epub(str(path.resolve()))

    title, _ = book.get_metadata("DC", "title")[0]
    creators = [i[0] for i in book.get_metadata("DC", "creator")]
    language, _ = book.get_metadata("DC", "language")[0]
    cover_image: EpubCover = book.get_item_with_id("cover-image")

    book = Book(
        title=title,
        local_path=str(path.resolve()),
        creators=creators,
        language=language,
    )

    if cover_image:
        file_ext = cover_image.file_name.split(".")[-1]
        file_name = f"{book.id}.{file_ext}"
        img_path = Path(ORIGINALS_DIR, file_name)

        with open(img_path, "wb") as fp:
            fp.write(cover_image.get_content())

        with open_img(img_path) as img:
            for size, outpath in ((SM, SM_DIR), (MD, MD_DIR), (LG, LG_DIR)):
                thumb = img.copy()
                thumb.thumbnail(size)
                thumb.save(Path(outpath, file_name))

    return book


def parse_library():
    for file in glob("**/*.epub", root_dir=DATA_DIR.resolve(), recursive=True):
        book = make_book(Path(DATA_DIR, file))
        book.to_record()


def get_book(id: str) -> Book:
    return Book.from_record(id)


def list_books() -> List[Book]:
    keys = [i["id"] for i in db.all()]

    return [Book.from_record(i) for i in keys]


def get_book_path(id: str) -> str:
    book = Book.from_record(id)

    return book.local_path


if __name__ == "__main__":
    parse_library()
