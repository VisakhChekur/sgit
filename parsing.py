from argparse import ArgumentParser

from typings import SubparserCommand



subparser_commands: dict[str, SubparserCommand] = {
    "init": {
        "help": "Initialize empty repository",
        "sub_cmds": [{
            "command_name": "path",
            "help": "Path to initialize the repository"
        }]
    }
}



def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Main command")
    sub_parser = parser.add_subparsers(title="Commands", dest="command", help="Sub command")

    # Adding subparser commands
    for cmd, details in subparser_commands.items():
        sub_sub_parser = sub_parser.add_parser(cmd, help=details["help"])
        for sub_cmd in details["sub_cmds"]:
            sub_sub_parser.add_argument(sub_cmd["command_name"], help=sub_cmd["help"])

    sub_parser.required = True

    return parser

