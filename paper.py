from utils.data_utils import arxiv_download, extract_num
from utils.api_queries import get_entry, parse_entry


class ArxivPaper:
    metadata = None
    loc = None

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
        paper = cls(number)
        paper.loc = path
        return paper

    @property
    def authors(self):
        if self.metadata is None:
            self.get_metadata()
        return self.metadata["authors"]

    @property
    def abstract(self):
        if self.metadata is None:
            self.get_metadata()
        return self.metadata["abstract"]

    @property
    def title(self):
        if self.metadata is None:
            self.get_metadata()
        return self.metadata["title"]

    @property
    def category(self):
        if self.metadata is None:
            self.get_metadata()
        return self.metadata["category"]

    def get_metadata(self):
        entry = get_entry(self.number)
        self.metadata = parse_entry(entry)

    def download(self, path):
        arxiv_download(self.file_url, path)
        self.loc = path
