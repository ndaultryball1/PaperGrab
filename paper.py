from papergrab import arxiv_download, extract_num, get_author
from api_queries import get_entry, parse_entry

class ArxivPaper:
    _author = None
    _title = None
    _abstract = None
    _date = None

    def __init__(self, number):
        self.number = number

    @property
    def file_url(self):
        return "https://export.arxiv.org/pdf/" + self.number + ".pdf"

    @property
    def page_url(self):
        return "https://export.arxiv.org/abs/" + self.number

    @classmethod
    def from_file(cls, path):
        number = extract_num(path)
        return cls(number)

    @property
    def authors(self):
        if self._author is not None:
            return self._author
        else:
            self.get_metadata()
            return self._author

    def get_metadata(self):
        entry = get_entry(self.number)
        data = parse_entry(entry)
        self._author = data["authors"]
        self._title = data["title"]
        self._abstract = data["abstract"]


    def download(self, path):
        arxiv_download(self.file_url, path)