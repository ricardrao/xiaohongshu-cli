"""Interaction commands: like, collect, comment, reply."""

import click

from ..cookies import get_cookies
from ..client import XhsClient
from ..exceptions import XhsApiError, NoCookieError
from ..formatter import extract_note_id, print_error, print_json, print_success


def _get_client(ctx) -> XhsClient:
    cookie_source = ctx.obj.get("cookie_source", "chrome") if ctx.obj else "chrome"
    cookies = get_cookies(cookie_source)
    return XhsClient(cookies)


@click.command()
@click.argument("id_or_url")
@click.option("--undo", is_flag=True, help="Unlike instead of like")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def like(ctx, id_or_url: str, undo: bool, as_json: bool):
    """Like or unlike a note."""
    note_id = extract_note_id(id_or_url)

    try:
        with _get_client(ctx) as client:
            if undo:
                data = client.unlike_note(note_id)
                if as_json:
                    print_json(data)
                else:
                    print_success(f"Unliked note {note_id}")
            else:
                data = client.like_note(note_id)
                if as_json:
                    print_json(data)
                else:
                    print_success(f"Liked note {note_id}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("id_or_url")
@click.option("--undo", is_flag=True, help="Uncollect instead of collect")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def collect(ctx, id_or_url: str, undo: bool, as_json: bool):
    """Collect (bookmark) or uncollect a note."""
    note_id = extract_note_id(id_or_url)

    try:
        with _get_client(ctx) as client:
            if undo:
                data = client.uncollect_note(note_id)
                if as_json:
                    print_json(data)
                else:
                    print_success(f"Uncollected note {note_id}")
            else:
                data = client.collect_note(note_id)
                if as_json:
                    print_json(data)
                else:
                    print_success(f"Collected note {note_id}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("id_or_url")
@click.option("--content", "-c", required=True, help="Comment content")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def comment(ctx, id_or_url: str, content: str, as_json: bool):
    """Post a comment on a note."""
    note_id = extract_note_id(id_or_url)

    try:
        with _get_client(ctx) as client:
            data = client.post_comment(note_id, content)

        if as_json:
            print_json(data)
        else:
            print_success(f"Comment posted on {note_id}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("id_or_url")
@click.option("--comment-id", required=True, help="Target comment ID to reply to")
@click.option("--content", "-c", required=True, help="Reply content")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def reply(ctx, id_or_url: str, comment_id: str, content: str, as_json: bool):
    """Reply to a specific comment."""
    note_id = extract_note_id(id_or_url)

    try:
        with _get_client(ctx) as client:
            data = client.reply_comment(note_id, comment_id, content)

        if as_json:
            print_json(data)
        else:
            print_success(f"Reply posted on comment {comment_id}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)
