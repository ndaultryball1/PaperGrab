import pytest
from paper import ArxivPaper
from utils.data_utils import extract_num
import os

eg_id = "2004.01128"


@pytest.fixture(scope="session")
def paper_example() -> ArxivPaper:
    return ArxivPaper(eg_id)


@pytest.fixture(scope="session")
def paper_loc(tmpdir_factory):
    directory = tmpdir_factory.mktemp("paper").join("eg.pdf")
    return directory


class TestArxivPaper:
    def test_download(self, paper_loc, paper_example):
        paper_example.download(paper_loc)
        assert os.path.exists(paper_loc)

    def test_from_number(self, paper_example):
        assert paper_example.number == eg_id

    def test_extract(self, paper_loc):
        assert extract_num(paper_loc) == eg_id
