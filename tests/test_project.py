import pytest
import os
from project import Project
from paper import ArxivPaper
from utils.exceptions import ProjectNotFound


eg_id = "2004.01128"


@pytest.fixture(scope="session")
def paper_example() -> ArxivPaper:
    return ArxivPaper(eg_id)


@pytest.fixture(scope="session")
def project_loc(tmpdir_factory):
    return tmpdir_factory.mktemp("project_eg")

@pytest.fixture()
def ran_loc(tmpdir_factory):
    return tmpdir_factory.mktemp("ran_dir")

@pytest.fixture()
def paper_loc(project_loc):
    return project_loc.join("paper.pdf")


@pytest.fixture(scope="session")
def eg_project(project_loc):
    return Project(project_loc)


class TestProject:
    def test_create_db(self, eg_project):
        eg_project.create_db()
        assert os.path.exists(eg_project.server)

    def test_add(self, paper_example, eg_project, paper_loc):
        paper_example.download(paper_loc)
        eg_project.add(paper_example)

    def test_load(self, eg_project):
        project = Project.load(eg_project.root)
        assert isinstance(project, Project)

    def test_fail_load(self, ran_loc):
        with pytest.raises(ProjectNotFound):
            _ = Project.load(ran_loc)

    def test_retrieve(self, eg_project, paper_loc):
        record = eg_project.load_id(eg_id)
        assert record.loc == paper_loc
        assert record.id == eg_id


