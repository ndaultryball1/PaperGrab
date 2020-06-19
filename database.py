import sqlite3
from collections import namedtuple


def gen_schema(values):
    return "(" + ", ".join(values) + ")"


def empty_schema(length):
    return gen_schema(["?"]*length)


def string_schema(schema):
    keys = schema._fields
    keys_with_types = [key + " text" for key in keys]
    return gen_schema(keys_with_types)


class Database:
    def __init__(self, location: str, schema: namedtuple):
        self.location = location
        self.schema = schema
        self.db_name = schema.__name__ + "s"

    def __enter__(self):
        self.conn = sqlite3.connect(self.location)
        self.conn.row_factory = self.row_factory
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.conn.commit()
        self.conn.close()

    def __call__(self, instruction, *args, **kwargs):
        self.cursor.execute(instruction, *args, **kwargs)

    def row_factory(self, cursor, row):
        return self.schema(*row)

    def instantiate(self):
        schema = string_schema(self.schema)
        command = f"""CREATE TABLE IF NOT EXISTS {self.db_name} """ + schema
        with self as db:
            db(command)

    def add_record(self, record: namedtuple):
        with self as db:
            db(f"INSERT INTO {self.db_name} VALUES " + empty_schema(len(record)), record)

    def fetch_id(self, id: str):
        with self as db:
            db(f"SELECT * FROM {self.db_name} WHERE id = (?)", (id,))
            data = db.cursor.fetchone()
        return data