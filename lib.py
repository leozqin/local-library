from pathlib import Path
from typing import List
from pydantic import BaseModel
from hashlib import md5
from os import environ
from glob import glob

from PIL.Image import open as open_img, Image
from ebooklib.epub import read_epub, EpubBook, IMAGE_MEDIA_TYPES, EpubCover
from ebooklib import ITEM_COVER

DATA_DIR = Path(environ.get("DATA_DIR", Path(__file__).parent.joinpath("data")))
print(DATA_DIR)

COVERS_DIR = Path(DATA_DIR, "covers")

ORIGINALS_DIR = Path(COVERS_DIR, "originals")
ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)

SM_DIR = Path(COVERS_DIR, "sm")
SM_DIR.mkdir(parents=True, exist_ok=True)
MD_DIR = Path(COVERS_DIR, "md")
MD_DIR.mkdir(parents=True, exist_ok=True)
LG_DIR = Path(COVERS_DIR, "lg")
LG_DIR.mkdir(parents=True, exist_ok=True)

SM = 200,200
MD = 400,400
LG = 600,600

class Book(BaseModel):
    title: str
    creators: List[str]
    local_path: Path
    language: str = "en"
    

    @property
    def id(self):
        path = self.local_path.resolve()
        return md5(str(path).encode()).hexdigest()

def make_book(path: Path) -> Book:
    book = read_epub(str(path.resolve()))

    title, _ = book.get_metadata("DC", "title")[0]
    creators  = [i[0] for i in book.get_metadata("DC", "creator")]
    language, _ = book.get_metadata("DC", "language")[0]
    cover_image: EpubCover = book.get_item_with_id('cover-image')

    book = Book(
        title=title,
        local_path=path.resolve(),
        creators=creators,
        language=language
    )

    if cover_image:
        print(cover_image.file_name)
        print(cover_image.media_type)
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
        print(book.model_dump())

if __name__ == "__main__":
    parse_library()