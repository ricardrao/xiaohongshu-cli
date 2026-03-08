"""Social graph commands: followers, following, follow, unfollow."""

import click

from ..cookies import get_cookies
from ..client import XhsClient
from ..exceptions import XhsApiError, NoCookieError
from ..formatter import print_error, print_json, print_success, print_info, render_users


def _get_client(ctx) -> XhsClient:
    cookie_source = ctx.obj.get("cookie_source", "chrome") if ctx.obj else "chrome"
    cookies = get_cookies(cookie_source)
    return XhsClient(cookies)


@click.command()
@click.argument("user_id")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def followers(ctx, user_id: str, cursor: str, as_json: bool):
    """List a user's followers."""
    try:
        with _get_client(ctx) as client:
            data = client.get_user_followers(user_id, cursor=cursor)

        if as_json:
            print_json(data)
        else:
            render_users(data)
            if data and isinstance(data, dict) and data.get("has_more"):
                next_cursor = data.get("cursor", "")
                print_info(f"More followers — use --cursor {next_cursor}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("user_id")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def following(ctx, user_id: str, cursor: str, as_json: bool):
    """List a user's following."""
    try:
        with _get_client(ctx) as client:
            data = client.get_user_following(user_id, cursor=cursor)

        if as_json:
            print_json(data)
        else:
            render_users(data)
            if data and isinstance(data, dict) and data.get("has_more"):
                next_cursor = data.get("cursor", "")
                print_info(f"More following — use --cursor {next_cursor}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("user_id")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def follow(ctx, user_id: str, as_json: bool):
    """Follow a user."""
    try:
        with _get_client(ctx) as client:
            data = client.follow_user(user_id)

        if as_json:
            print_json(data)
        else:
            print_success(f"Followed user {user_id}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command()
@click.argument("user_id")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def unfollow(ctx, user_id: str, as_json: bool):
    """Unfollow a user."""
    try:
        with _get_client(ctx) as client:
            data = client.unfollow_user(user_id)

        if as_json:
            print_json(data)
        else:
            print_success(f"Unfollowed user {user_id}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command("user-collects")
@click.argument("user_id")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def user_collects(ctx, user_id: str, cursor: str, as_json: bool):
    """List a user's collected (bookmarked) notes."""
    try:
        with _get_client(ctx) as client:
            data = client.get_user_collects(user_id, cursor=cursor)

        if as_json:
            print_json(data)
        else:
            from ..formatter import render_user_posts
            notes = data.get("notes", []) if isinstance(data, dict) else []
            render_user_posts(notes)
            if isinstance(data, dict) and data.get("has_more"):
                print_info(f"More notes — use --cursor {data.get('cursor', '')}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)


@click.command("user-likes")
@click.argument("user_id")
@click.option("--cursor", default="", help="Pagination cursor")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def user_likes(ctx, user_id: str, cursor: str, as_json: bool):
    """List a user's liked notes."""
    try:
        with _get_client(ctx) as client:
            data = client.get_user_likes(user_id, cursor=cursor)

        if as_json:
            print_json(data)
        else:
            from ..formatter import render_user_posts
            notes = data.get("notes", []) if isinstance(data, dict) else []
            render_user_posts(notes)
            if isinstance(data, dict) and data.get("has_more"):
                print_info(f"More notes — use --cursor {data.get('cursor', '')}")

    except (NoCookieError, XhsApiError) as e:
        print_error(str(e))
        raise SystemExit(1)
