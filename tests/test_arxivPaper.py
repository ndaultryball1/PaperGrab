import pytest
from paper import ArxivPaper
import os

eg_id = "2004.01128"


@pytest.fixture()
def paper_example() -> ArxivPaper:
    return ArxivPaper(eg_id)


class TestArxivPaper:
    def test_download(self, tmpdir, paper_example):
        new_path = os.path.join(tmpdir, "paper_" + eg_id)
        assert paper_example.number == eg_id
        paper_example.download(new_path)
        assert os.path.exists(new_path)
