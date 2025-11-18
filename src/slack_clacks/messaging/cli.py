import argparse
import json
import sys

from slack_sdk import WebClient

from slack_clacks.configuration.database import (
    ensure_db_updated,
    get_current_context,
    get_session,
)

from .operations import (
    open_dm_channel,
    resolve_channel_id,
    resolve_user_id,
    send_message,
)


def handle_send(args: argparse.Namespace) -> None:
    ensure_db_updated(config_dir=args.config_dir)
    with get_session(args.config_dir) as session:
        context = get_current_context(session)
        if context is None:
            raise ValueError(
                "No active authentication context. Authenticate with: clacks auth login"
            )

        client = WebClient(token=context.access_token)

        channel_id = None

        if args.channel:
            channel_id = resolve_channel_id(client, args.channel)
            if channel_id is None:
                raise ValueError(f"Channel '{args.channel}' not found.")
        elif args.user:
            user_id = resolve_user_id(client, args.user)
            if user_id is None:
                raise ValueError(f"User '{args.user}' not found.")
            channel_id = open_dm_channel(client, user_id)
            if channel_id is None:
                raise ValueError(f"Failed to open DM with user '{args.user}'.")
        else:
            raise ValueError("Must specify either --channel or --user.")

        response = send_message(client, channel_id, args.message, thread_ts=args.thread)

        output = {
            "status": "success",
            "timestamp": response["ts"],
            "channel": response["channel"],
        }
        with args.outfile as ofp:
            json.dump(output, ofp)


def generate_send_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Send a message",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-D",
        "--config-dir",
        type=str,
        help="Configuration directory (default: platform-specific user config dir)",
    )
    parser.add_argument(
        "-c",
        "--channel",
        type=str,
        help="Channel ID or name (e.g., #general, C123456)",
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        help="User ID or name for DM (e.g., @username, U123456)",
    )
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        required=True,
        help="Message text",
    )
    parser.add_argument(
        "-t",
        "--thread",
        type=str,
        help="Thread timestamp for replying to thread",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("a"),
        default=sys.stdout,
        help="Output file for JSON results (default: stdout)",
    )
    parser.set_defaults(func=handle_send)

    return parser
