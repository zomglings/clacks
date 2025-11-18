import argparse

from slack_clacks.configuration.cli import generate_cli as generate_init_cli


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="clacks: Control Slack from your command line"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    init_parser = generate_init_cli()
    subparsers.add_parser(
        "init", parents=[init_parser], add_help=False, help=init_parser.description
    )

    return parser
