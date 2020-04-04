import sqlite3
from paper import ArxivPaper
from collections import namedtuple

Record = namedtuple(
    "Record", ["title", "first_author", "category", "id", "loc", "abstract"]
)


class Project:
    def __init__(self, dir):
        self.root = dir
        self.server = dir + "/grab.db"
        conn = sqlite3.connect(dir + "/grab.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE papers
                     (title text, first_author text, category text,id text, loc text, abstract text)"""
        )
        conn.commit()
        conn.close()

    def add(self, file):
        conn = sqlite3.connect(self.server)
        c = conn.cursor()
        paper = ArxivPaper.from_file(file)
        data = Record(
            title=paper.title,
            first_author=paper.author[0],
            category=paper.category,
            id=paper.number,
            loc=file,
            abstract=paper.abstract,
        )
        c.execute("INSERT INTO papers VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
