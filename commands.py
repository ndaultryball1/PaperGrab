"""
Defines functions for the different modes of operation of the command line tool
"""
from project import Project
from paper import ArxivPaper
import os


def get_all_in_dir(directory) -> [ArxivPaper]:
    good_paths = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            good_paths.append(os.path.join(root, name))
    return [ArxivPaper.from_file(path) for path in good_paths]


def new(args):
    """
    Creates and initialises a new project
    :return:
    """
    cwd = os.getcwd()
    new_project = Project(cwd)
    new_project.create_db()
    if args.a:
        papers = get_all_in_dir(cwd)
        for paper in papers:
            new_project.add(paper)


def add(args):
    """
    Adds a paper to an existing project
    :param args:
    :return:
    """
    paths = args.files
    cwd = os.getcwd()
    project = Project.get_current_project(cwd)
    files_list = [os.path.join(cwd, path) for path in paths]

