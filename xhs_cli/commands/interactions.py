"""Interaction commands: like, collect, comment, reply, report."""

import click

from ..cookies import cache_note_context
from ..formatter import print_success
from ..note_refs import resolve_note_reference
from ._common import handle_command, structured_output_options


def _resolve_interaction_note(id_or_url: str) -> str:
    note_id, token, source = resolve_note_reference(id_or_url)
    if token:
        cache_note_context(note_id, token, source or "pc_feed")
    return note_id


@click.command()
@click.argument("id_or_url")
@click.option("--undo", is_flag=True, help="Unlike instead of like")
@structured_output_options
@click.pass_context
def like(ctx, id_or_url: str, undo: bool, as_json: bool, as_yaml: bool):
    """Like or unlike a note."""
    note_id = _resolve_interaction_note(id_or_url)
    action = (lambda client: client.unlike_note(note_id)) if undo else (lambda client: client.like_note(note_id))
    handle_command(
        ctx,
        action=action,
        render=lambda _data: print_success(f"{'Unliked' if undo else 'Liked'} note {note_id}"),
        as_json=as_json,
        as_yaml=as_yaml,
    )


@click.command()
@click.argument("id_or_url")
@structured_output_options
@click.pass_context
def favorite(ctx, id_or_url: str, as_json: bool, as_yaml: bool):
    """Favorite (bookmark) a note."""
    note_id = _resolve_interaction_note(id_or_url)
    handle_command(
        ctx,
        action=lambda client: client.favorite_note(note_id),
        render=lambda _data: print_success(f"Favorited note {note_id}"),
        as_json=as_json,
        as_yaml=as_yaml,
    )


@click.command()
@click.argument("id_or_url")
@structured_output_options
@click.pass_context
def unfavorite(ctx, id_or_url: str, as_json: bool, as_yaml: bool):
    """Unfavorite (unbookmark) a note."""
    note_id = _resolve_interaction_note(id_or_url)
    handle_command(
        ctx,
        action=lambda client: client.unfavorite_note(note_id),
        render=lambda _data: print_success(f"Unfavorited note {note_id}"),
        as_json=as_json,
        as_yaml=as_yaml,
    )


@click.command()
@click.argument("id_or_url")
@click.option("--content", "-c", required=True, help="Comment content")
@structured_output_options
@click.pass_context
def comment(ctx, id_or_url: str, content: str, as_json: bool, as_yaml: bool):
    """Post a comment on a note."""
    note_id = _resolve_interaction_note(id_or_url)
    handle_command(
        ctx,
        action=lambda client: client.post_comment(note_id, content),
        render=lambda _data: print_success(f"Comment posted on {note_id}"),
        as_json=as_json,
        as_yaml=as_yaml,
    )


@click.command()
@click.argument("id_or_url")
@click.option("--comment-id", required=True, help="Target comment ID to reply to")
@click.option("--content", "-c", required=True, help="Reply content")
@structured_output_options
@click.pass_context
def reply(ctx, id_or_url: str, comment_id: str, content: str, as_json: bool, as_yaml: bool):
    """Reply to a specific comment."""
    note_id = _resolve_interaction_note(id_or_url)
    handle_command(
        ctx,
        action=lambda client: client.reply_comment(note_id, comment_id, content),
        render=lambda _data: print_success(f"Reply posted on comment {comment_id}"),
        as_json=as_json,
        as_yaml=as_yaml,
    )


@click.command("delete-comment")
@click.argument("note_id")
@click.argument("comment_id")
@structured_output_options
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
@click.pass_context
def delete_comment(ctx, note_id: str, comment_id: str, as_json: bool, as_yaml: bool, yes: bool):
    """Delete a comment you posted."""
    if not yes:
        click.confirm(f"Delete comment {comment_id} on note {note_id}?", abort=True)

    handle_command(
        ctx,
        action=lambda client: client.delete_comment(note_id, comment_id),
        render=lambda _data: print_success(f"Deleted comment {comment_id}"),
        as_json=as_json,
        as_yaml=as_yaml,
    )


@click.command("report")
@click.argument("id_or_url")
@click.option("--target-user-id", required=True, help="Author user ID of the target note")
@click.option("--report-item-id", required=True, help="Top-level report category ID (e.g. porn)")
@click.option("--single-item-id", required=True, help="Second-level report category ID")
@click.option("--reason", default="", help="Reason text used for both report_item and single_item")
@click.option("--report-reason", default=None, help="Override reason text for report_item")
@click.option("--single-reason", default=None, help="Override reason text for single_item")
@click.option("--scenario-id", default="note_web", show_default=True, help="Report scenario ID")
@click.option("--description", default="", help="Additional report description")
@structured_output_options
@click.pass_context
def report(
    ctx,
    id_or_url: str,
    target_user_id: str,
    report_item_id: str,
    single_item_id: str,
    reason: str,
    report_reason: str | None,
    single_reason: str | None,
    scenario_id: str,
    description: str,
    as_json: bool,
    as_yaml: bool,
):
    """Report a note."""
    note_id = _resolve_interaction_note(id_or_url)
    final_report_reason = reason if report_reason is None else report_reason
    final_single_reason = reason if single_reason is None else single_reason

    handle_command(
        ctx,
        action=lambda client: client.report_note(
            note_id=note_id,
            target_user_id=target_user_id,
            report_item_id=report_item_id,
            single_item_id=single_item_id,
            scenario_id=scenario_id,
            report_reason=final_report_reason,
            single_reason=final_single_reason,
            description=description,
        ),
        render=lambda _data: print_success(f"Reported note {note_id}"),
        as_json=as_json,
        as_yaml=as_yaml,
    )
