import sys

from parsing import create_parser
import command_handlers

def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    
    match args.command:

        case "init":
            command_handlers.handle_init(args.path)
        case _:
            print("Invalid command")
            return


if __name__ == "__main__":
    main()