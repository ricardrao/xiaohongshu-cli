"""Reading commands: search, read, comments, user, user-posts, feed, topics."""

import click

from ..cookies import get_cookies
from ..client import XhsClient
from ..exceptions import XhsApiError, NoCookieError
from ..formatter import (
    extract_note_id,
    print_error,
    print_json,
    print_info,
    render_comments,
    render_feed,
    render_note,
    render_search_results,
    render_topics,
    render_user_info,
    render_user_posts,
)


def _get_client(ctx) -> XhsClient:
    """Get an XhsClient from the click context."""
    cookie_source = ctx.obj.get("cookie_source", "chrome") if ctx.obj else "chrome"
    cookies = get_cookies(cookie_source)
    return XhsClient(cookies)


# ─── Sort mapping ────────────────────────────────────────────────────────────

SORT_MAP = {
    "general": "general",
    "popular": "popularity_descending",
    "latest": "time_descending",
}

TYPE_MAP = {
    "all": 0,
    "video": 1,
    "image": 2,
}


@click.command()
@click.argument("keyword")
@click.option("--sort", type=click.Choice(["general", "popular", "latest"]), default="general", help="Sort order")
@click.option("--type", "note_type", type=click.Choice(["all", "video", "image"]), default="all", help="Note type")
@click.option("--page", default=1, help="Page number")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def search(ctx, keyword: str, sort: str, note_type: str, page: int, as_json: bool):
    """Search notes by keyword."""
    try:
        with _get_client(ctx) as client:
            data = client.search_notes(
                keyword=keyword,
                page=page,
                sort=SORT_MAP[sort],
                note_type=TYPE_MAP[note_type],
            )

        if as_json:
            print_json(data)
        else:
            render_search_results(data)

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("id_or_url")
@click.option("--xsec-token", default="", help="Security token (auto-resolved if cached)")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def read(ctx, id_or_url: str, xsec_token: str, as_json: bool):
    """Read a note by ID or URL."""
    note_id = extract_note_id(id_or_url)

    try:
        with _get_client(ctx) as client:
            data = client.get_note_by_id(note_id, xsec_token=xsec_token)

        if as_json:
            print_json(data)
        else:
            render_note(data)

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("id_or_url")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--xsec-token", default="", help="Security token")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def comments(ctx, id_or_url: str, cursor: str, xsec_token: str, as_json: bool):
    """Get comments for a note."""
    note_id = extract_note_id(id_or_url)

    try:
        with _get_client(ctx) as client:
            data = client.get_comments(note_id, cursor=cursor, xsec_token=xsec_token)

        if as_json:
            print_json(data)
        else:
            render_comments(data)

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("user_id")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def user(ctx, user_id: str, as_json: bool):
    """View user profile info."""
    try:
        with _get_client(ctx) as client:
            data = client.get_user_info(user_id)

        if as_json:
            print_json(data)
        else:
            render_user_info(data)

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command("user-posts")
@click.argument("user_id")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def user_posts(ctx, user_id: str, cursor: str, as_json: bool):
    """List a user's published notes."""
    try:
        with _get_client(ctx) as client:
            data = client.get_user_notes(user_id, cursor=cursor)

        if as_json:
            print_json(data)
        else:
            notes = data.get("notes", [])
            render_user_posts(notes)
            if data.get("has_more"):
                cursor = data.get("cursor", "")
                print_info(f"More notes available — use --cursor {cursor}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def feed(ctx, as_json: bool):
    """Browse the recommendation feed."""
    try:
        with _get_client(ctx) as client:
            data = client.get_home_feed()

        if as_json:
            print_json(data)
        else:
            render_feed(data)

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("keyword")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def topics(ctx, keyword: str, as_json: bool):
    """Search for topics/hashtags."""
    try:
        with _get_client(ctx) as client:
            data = client.search_topics(keyword)

        if as_json:
            print_json(data)
        else:
            render_topics(data)

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)
