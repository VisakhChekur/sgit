from typing import TypedDict

class SubCommand(TypedDict):

    command_name: str
    help: str

class SubparserCommand(TypedDict):

    help: str
    sub_cmds: list[SubCommand]
