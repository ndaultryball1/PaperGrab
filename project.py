import sqlite3
from paper import ArxivPaper
from collections import namedtuple

Record = namedtuple(
    "Record", ["title", "first_author", "category", "id", "loc", "abstract"]
)

def record_factory(cursor, row):
    return Record(*row)

class Project:
    def __init__(self, dir):
        self.root = dir
        self.server = dir + "/grab.db"

    def create_db(self):
        conn = sqlite3.connect(self.server)  # TODO: turn this into a coroutine with a finally clause
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
            loc=str(paper.loc),
            abstract=paper.abstract,
        )
        c.execute("INSERT INTO papers VALUES (?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()

    def load_id(self, id):
        conn = sqlite3.connect(self.server)
        conn.row_factory = record_factory
        c = conn.cursor()
        c.execute("SELECT * FROM papers WHERE id = (?)", (id,))
        return c.fetchone()
