from papergrab import arxiv_download, extract_num


class ArxivPaper:
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

    def download(self, path):
        arxiv_download(self.file_url, path)