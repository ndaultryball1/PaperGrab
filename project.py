import os
from paper import ArxivPaper
from collections import namedtuple
from database import Database
DB_FILENAME = "grab.db"

class ProjectNotFound(FileNotFoundError):
    pass

Record = namedtuple(
    "Record", ["title", "first_author", "category", "id", "loc", "abstract"]
)


class Project:
    def __init__(self, dir):
        self.root = dir
        self.server = os.path.join(dir, DB_FILENAME)
        self.database = Database(location=self.server, schema=Record)

    def create_db(self):
        self.database.instantiate()

    def add(self, paper: ArxivPaper):
        # Adds a paper to an existing project.

        data = Record(
            title=paper.title,
            first_author=paper.authors[0],
            category=paper.category,
            id=paper.id,
            loc=str(paper.loc),
            abstract=paper.abstract,
        )
        self.database.add_record(data)

    def load_id(self, id):
        return self.database.fetch_id(id)

    @classmethod
    def load(cls, dir):
        if os.path.exists(os.path.join(dir, DB_FILENAME)):
            return Project(dir)
        else:
            raise ProjectNotFound

    @classmethod
    def get_current_project(cls, dir):
        found = False
        while not found:
            try:
                cls.load(dir)
            except ProjectNotFound:
                newdir = os.path.join(dir, os.pardir)
                if newdir == dir:
                    # Reached top of file structure without locating
                    raise ProjectNotFound
                else:
                    dir = newdir