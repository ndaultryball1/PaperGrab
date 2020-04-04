import sqlite3
from paper import ArxivPaper

class Project:
    def __init__(self, dir):
        self.root = dir
        self.conn = sqlite3.connect(dir + "/grab.db")

    def add(self, paper):
        self.conn