import commands
import argparse

parser = argparse.ArgumentParser(
    description="Collect and interact with ArXiV research papers."
)
subparser = parser.add_subparsers()


parser_new = subparser.add_parser(
    "new", help="Create a new project in the current directory"
)
parser_new.add_argument(
    "-a",
    help="If present, populates the db with all papers in the current directory",
    action="store_true",
)
parser_new.set_defaults(func=commands.new)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)
