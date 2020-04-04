import urllib3
import shutil
import PyPDF2
import re
import logging

logger = logging.getLogger(__name__)
id_regex = re.compile("[0-9]{4}\.[0-9]+")


def arxiv_download(url, path):
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
    # Arxiv rejects requests without a user agent
    http = urllib3.PoolManager(headers=user_agent)
    with http.request("GET", url, preload_content=False) as r, open(path, "wb") as out:
        shutil.copyfileobj(r, out)

    logger.debug(f"Downloaded {url} to {path}")


def find_id(string):
    match = id_regex.search(string)
    if match is not None:
        return match.group()
    else:
        raise ValueError("No ID in string")


def extract_num(path):
    with open(path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        first_page = reader.getPage(0)
        text = first_page.extractText()
        return find_id(text)


if __name__ == "__main__":
    eg_path = "C://Users//Nicholas//example.pdf"
    arxiv_download("https://export.arxiv.org/pdf/2004.01128v1.pdf", eg_path)
    print(extract_num(eg_path))