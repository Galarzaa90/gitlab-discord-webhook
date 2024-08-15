import configparser
import json
from collections.abc import AsyncIterator
from io import BytesIO

import aiohttp
import discord
from aiohttp import web
from aiohttp_middlewares import (
    error_context,
    error_middleware,
)
from loguru import logger
from pydantic import ValidationError

from gitlab_discord_webhook import models
from gitlab_discord_webhook.models import IssueHookPayload, MergeRequestHookPayload, NoteHookPayload, PushHookPayload

config = configparser.ConfigParser()

routes = web.RouteTableDef()

client_session = web.AppKey("client_session", aiohttp.ClientSession)

EMPTY_COMMIT = "0000000000000000000000000000000000000000"


@routes.post("/")
async def handle_webhook(request: web.Request) -> web.Response:
    """Handle a webhook payload from GitLab.com."""
    try:
        event_type = request.headers.getone("x-gitlab-event")
    except KeyError:
        logger.error("Request is missing `x-gitlab-event` header.")
        return web.HTTPBadRequest(text="GitLab event type not found.")
    logger.info("Received `{}` event", event_type)
    body = await request.json()
    if event_type == "Push Hook":
        await process_push_hook(request.app, PushHookPayload.model_validate(body))
    if event_type == "Issue Hook":
        await process_issue_hook(request.app, IssueHookPayload.model_validate(body))
    if event_type == "Note Hook":
        await process_note_hook(request.app, NoteHookPayload.model_validate(body))
    if event_type == "Merge Request Hook":
        await process_merge_request_hook(request.app, MergeRequestHookPayload.model_validate(body))
    return web.Response(text="OK")


async def process_push_hook(app: aiohttp.web.Application, push: models.PushHookPayload) -> None:
    """Build and sends an embed message with new commits information."""
    repository = push.repository
    project = push.project
    commit_str = "commit" if push.total_commits_count == 1 else "commits"
    # Show link to commit compare if there's more than one commit
    if push.total_commits_count > 1:
        embed_url = f"{repository.homepage}/compare/{push.before[:7]}...{push.after[:7]}"
    else:
        embed_url = f"{repository.homepage}/commit/{push.after[:7]}"

    if push.before == EMPTY_COMMIT:
        embed = discord.Embed(
            title=f"{project.namespace}/{project.name}] New branch created `{push.branch}`",
            url=embed_url,
            colour=discord.Colour.light_grey(),
        )
        embed.set_thumbnail(url=push.project.avatar_url)
        embed.set_author(name=push.user_name, icon_url=push.user_avatar)
        await send_message(app[client_session], None, embed=embed)
    elif push.after == EMPTY_COMMIT:
        embed = discord.Embed(title=f"[{project.namespace}/{project.name}] Branch deleted {push.branch}",
                              url=embed_url, colour=discord.Colour.light_grey())
        embed.set_author(name=push.user_name, icon_url=push.user_avatar)
        await send_message(app[client_session], None, embed=embed, avatar_url=push.project.avatar_url)

    # If there are no commits, do not show a message
    if not push.total_commits_count:
        return

    embed = discord.Embed(
        title=f"[{project.namespace}/{project.name}:{push.branch}] {push.total_commits_count} new {commit_str}",
        url=embed_url,
        colour=discord.Colour.blurple(),
    )
    embed.set_author(name=push.user_name, icon_url=push.user_avatar)
    embed.set_thumbnail(url=push.project.avatar_url)
    embed.description = ""
    for commit in push.commits:
        message = commit.message.splitlines()[0]
        embed.description += f"[`{commit.id[:7]}`]({commit.url}) {message} - {commit.author.name}\n"
        embed.timestamp = commit.timestamp
    print("Sending push message")
    await send_message(app[client_session], None, embed=embed)


async def process_issue_hook(app: aiohttp.web.Application, issue_data: IssueHookPayload) -> None:
    """Build and sends an embed message with issues information."""
    project = issue_data.project
    issue = issue_data.issue
    user = issue_data.user
    description = ""
    action = "Issue updated"
    colour = discord.Colour.light_grey()
    if issue.action == "open":
        action = "Issue opened"
        description = issue.description
        colour = discord.Colour.green()
    elif issue.action == "close":
        action = "Issue closed"
        colour = discord.Colour.dark_grey()
    embed = discord.Embed(
        title=f"[{project.namespace}/{project.name}] {action}: #{issue.iid} {issue.title}",
        url=issue.url,
        description=description,
        colour=colour,
        timestamp=issue.created_at,
    )
    embed.set_author(name=user.username, icon_url=user.avatar_url)
    await send_message(app[client_session], None, embed=embed)


async def process_note_hook(app: aiohttp.web.Application, data: NoteHookPayload) -> None:
    """Build and sends an embed message with notes information."""
    note = data.note
    user = data.user
    project = data.project
    colour = discord.Colour.greyple()
    embed = discord.Embed(url=note.url, description=note.note, colour=colour)
    embed.set_author(name=user.username, icon_url=user.avatar_url)
    embed.timestamp = note.created_at
    if data.issue:
        issue = data.issue
        embed.title = f"[{project.namespace}/{project.name}] New comment on issue #{issue.iid}: {issue.title}"
    elif data.commit:
        commit = data.commit
        embed.title = f"[{project.namespace}/{project.name}] New comment on commit `{commit.id[:7]}`"
    elif data.merge_request:
        merge = data.merge_request
        embed.title = f"[{project.namespace}/{project.name}] New comment on merge request !{merge.iid}: {merge.title}"
    await send_message(app[client_session], None, embed=embed)


async def process_merge_request_hook(app: aiohttp.web.Application, data: MergeRequestHookPayload) -> None:
    """Build and sends an embed message with merge request information."""
    project = data.project
    merge = data.merge_request
    user = data.user
    action = "Merge request updated"
    embed = discord.Embed(
        url=merge.url,
        timestamp=merge.created_at,
    )
    embed.set_author(name=user.username, icon_url=user.avatar_url)
    embed.set_footer(text=f"{merge.source_branch} → {merge.target_branch}")
    if merge.action == "open":
        action = "Merge request opened"
        embed.description = merge.description
        embed.colour = discord.Colour.dark_green()
    elif merge.action == "close":
        action = "Merge request closed"
        embed.colour = discord.Colour.dark_grey()
    elif merge.action == "merge":
        action = "Merge request merged"
        embed.colour = discord.Colour(0x064787)
    embed.title = f"[{project.namespace}/{project.name}] {action}: !{merge.iid} {merge.title}"
    if merge.action == "open":
        if data.assignees:
            embed.add_field(name="Assignees", value="\n".join([f"- {label.username}" for label in data.assignees]))
        if data.reviewers:
            embed.add_field(name="Reviewers", value="\n".join([f"- {label.username}" for label in data.reviewers]))
        if merge.labels:
            embed.add_field(name="Labels", value="\n".join([f"- `{label.title}`" for label in merge.labels]))
    await send_message(app[client_session], None, embed=embed)


async def send_message(session: aiohttp.ClientSession, content, **kwargs) -> None:
    """Send a message through a Discord webhook."""
    try:
        webhook = discord.Webhook.from_url(config["Discord"]["webhook"], session=session)
        await webhook.send(content, **kwargs)
    except Exception as e:
        web.HTTPInternalServerError(text=str(e))


async def prepare_session(app: aiohttp.web.Application) -> AsyncIterator[None]:
    """Prepare the HTTP client session that will be used for all requests."""
    logger.info("Creating ClientSession.")
    app[client_session] = aiohttp.ClientSession()
    yield
    logger.info("Closing ClientSession.")
    await app[client_session].close()


async def error_handler(request: web.Request) -> web.Response:
    """Handle errors, responding with some information on it."""
    with error_context(request) as context:
        app = request.app
        if isinstance(context.err, ValidationError):
            await send_error_webhook(app[client_session], context.err)
            return web.Response(text=context.err.json(), status=400, content_type="application/json")
        logger.exception(context.message, exc_info=context.err)
        return web.json_response(context.data, status=context.status)


async def send_error_webhook(session: aiohttp.ClientSession, exception: Exception) -> None:
    """Send a message through the configured error webhook."""
    if "error_webhook" not in config["Discord"]:
        return
    webhook = discord.Webhook.from_url(config["Discord"]["error_webhook"], session=session)
    if isinstance(exception, ValidationError):
        parsed_json = json.loads(exception.json())
        pretty_json = json.dumps(parsed_json, indent=2)
        file_bytes = BytesIO(pretty_json.encode("utf-8"))
        file = discord.File(file_bytes, filename="error.json")
        await webhook.send("Error", file=file)


def main() -> None:
    """Start the HTTP server."""
    if not config.read("config.ini"):
        print("Could not find config file.")
        exit()
    app = web.Application(
        middlewares=[
            error_middleware(default_handler=error_handler, ignore_exceptions=web.HTTPNotFound),
        ],
    )
    app.add_routes(routes)
    app.cleanup_ctx.append(prepare_session)
    web.run_app(app, port=7400)


if __name__ == "__main__":
    main()
