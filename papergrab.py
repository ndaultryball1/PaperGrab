import commands
import argparse
import sys
from utils.exceptions import PaperGrabError

parser = argparse.ArgumentParser(
    description="Collect and interact with ArXiV research papers."
)
subparser = parser.add_subparsers()

# Parser for the new command
parser_new = subparser.add_parser(
    "new", help="Create a new project in the current directory"
)
parser_new.add_argument(
    "-a",
    help="If present, populates the db with all papers in the current directory",
    action="store_true",
)
parser_new.set_defaults(func=commands.new)

# Parser for the add command
parser_add = subparser.add_parser("add", help="add a new paper to the current project")
parser_add.add_argument(name="files", nargs="+")
parser_add.set_defaults(func=commands.add)

if __name__ == "__main__":
    args = parser.parse_args()
    try:
        args.func(args)
    except PaperGrabError as e:
        print(e)
        sys.exit(1)

    sys.exit(0)
