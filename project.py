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

    def create_db(self):
        conn = sqlite3.connect(dir + "/grab.db")  # TODO: turn this into a coroutine with a finally clause
        c = conn.cursor()
        c.execute(
            """CREATE TABLE papers
                     (title text, first_author text, category text,id text, loc text, abstract text)"""
        )
        conn.commit()
        conn.close()

    def add(self, paper: ArxivPaper):
        # Adds a paper to an existing project.
        conn = sqlite3.connect(self.server)
        c = conn.cursor()
        data = Record(
            title=paper.title,
            first_author=paper.authors[0],
            category=paper.category,
            id=paper.number,
            loc=paper.loc,
            abstract=paper.abstract,
        )
        c.execute("INSERT INTO papers VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
