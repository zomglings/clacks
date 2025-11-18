import argparse
from pathlib import Path

from slack_clacks.configuration.database import ensure_db_initialized


def handle_init(args: argparse.Namespace) -> None:
    config_dir = args.config_dir
    ensure_db_initialized(config_dir=config_dir)
    print(f"Initialized configuration database at {config_dir}")


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage clacks configuration databases"
    )
    parser.add_argument(
        "-D",
        "--config-dir",
        type=Path,
        default=None,
        help="Directory in which to store the configuration database",
    )
    parser.set_defaults(func=handle_init)
    return parser
