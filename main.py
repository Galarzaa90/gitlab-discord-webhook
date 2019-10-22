import configparser

import aiohttp
import discord
from aiohttp import web

import models

config = configparser.ConfigParser()

routes = web.RouteTableDef()

EMPTY_COMMIT = "0000000000000000000000000000000000000000"


@routes.post('/webhook/gitlab')
async def receive_webhook(request: web.Request):
    try:
        event_type = request.headers.getone('x-gitlab-event')
    except KeyError:
        return web.HTTPBadRequest(text="GitLab event type not found.")
    body = await request.json()
    if event_type == "Push Hook":
        data = models.PushHook(**body)
        await process_push_hook(data)
    if event_type == "Issue Hook":
        data = models.IssueHook(**body)
        await process_issue_hook(data)
    if event_type == "Note Hook":
        data = models.NoteHook(**body)
        await process_note_hook(data)
    if event_type == "Merge Request Hook":
        data = models.MergeRequestHook(**body)
        await process_merge_request_hook(data)
    return web.Response(text="OK")


async def process_push_hook(push: models.PushHook):
    """Builds and sends an embed message with new commits information."""
    repository = push.repository
    project = push.project
    commit_str = "commit" if push.total_commits_count == 1 else "commits"
    # Show link to commit compare if there's more than one commit
    if push.total_commits_count > 1:
        embed_url = f"{repository.homepage}/compare/{push.before[:7]}...{push.after[:7]}"
    else:
        embed_url = f"{repository.homepage}/commit/{push.after[:7]}"

    if push.before == EMPTY_COMMIT:
        embed = discord.Embed(title=f"[{project.namespace}/{project.name}] New branch created {push.branch}",
                              url=embed_url, colour=discord.Colour.light_grey())
        embed.set_author(name=push.user_name, icon_url=push.user_avatar)
        await send_message(None, embed=embed, avatar_url=push.project.avatar_url)
    elif push.after == EMPTY_COMMIT:
        embed = discord.Embed(title=f"[{project.namespace}/{project.name}] Branch deleted {push.branch}",
                              url=embed_url, colour=discord.Colour.light_grey())
        embed.set_author(name=push.user_name, icon_url=push.user_avatar)
        await send_message(None, embed=embed, avatar_url=push.project.avatar_url)

    # If there are no commits, do not show a message
    if not push.total_commits_count:
        return

    embed = discord.Embed(title=f"[{project.namespace}/{project.name}:{push.branch}] "
                                f"{push.total_commits_count} new {commit_str}",
                          url=embed_url, colour=discord.Colour.blurple())
    embed.set_author(name=push.user_name, icon_url=push.user_avatar)
    embed.description = ""
    for commit in push.commits:
        message = commit.message.splitlines()[0]
        embed.description += f"[`{commit.id[:7]}`]({commit.url}) {message} - {commit.author.name}\n"
    print("Sending push message")
    await send_message(None, embed=embed, avatar_url=push.project.avatar_url)


async def process_issue_hook(issue_data):
    """Builds and sends an embed message with issues information."""
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
    embed = discord.Embed(title=f"[{project.namespace}/{project.name}] {action}: #{issue.iid} {issue.title}"
                          , url=issue.url, description=description, colour=colour)
    embed.set_author(name=user.username, icon_url=user.avatar_url)
    await send_message(None, embed=embed)


async def process_note_hook(data: models.NoteHook):
    """Builds and sends an embed message with notes information."""
    note = data.note
    user = data.user
    project = data.project
    colour = discord.Colour.greyple()
    embed = discord.Embed(url=note.url, description=note.description, colour=colour)
    embed.set_author(name=user.username, icon_url=user.avatar_url)
    if data.issue:
        issue = data.issue
        embed.title = f"[{project.namespace}/{project.name}] New comment on issue #{issue.iid}: {issue.title}"
    if data.commit:
        commit = data.commit
        embed.title = f"[{project.namespace}/{project.name}] New comment on commit `{commit.id[:7]}`"
    if data.merge_request:
        merge = data.merge_request
        embed.title = f"[{project.namespace}/{project.name}] New comment on merge request !{merge.iid}: {merge.title}"
    await send_message(None, embed=embed)


async def process_merge_request_hook(data: models.MergeRequestHook):
    """Builds and sends an embed message with merge request information."""
    project = data.project
    merge = data.merge_request
    user = data.user
    description = ""
    action = "Issue updated"
    colour = discord.Colour.light_grey()
    if merge.action == "open":
        action = "Merge request opened"
        description = merge.description
        colour = discord.Colour.dark_green()
    elif merge.action == "close":
        action = "Merge request closed"
        colour = discord.Colour.dark_grey()
    embed = discord.Embed(title=f"[{project.namespace}/{project.name}] {action}: !{merge.iid} {merge.title}",
                          url=merge.url, description=description, colour=colour)
    embed.set_author(name=user.username, icon_url=user.avatar_url)
    embed.set_footer(text=f"{merge.source_branch} → {merge.target_branch}")
    await send_message(None, embed=embed)


async def send_message(content, **kwargs):
    async with aiohttp.ClientSession() as session:
        try:
            webhook = discord.Webhook.from_url(config['Discord']['webhook'],
                                               adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(content, **kwargs)
        except Exception as e:
            web.HTTPInternalServerError(text=str(e))


if __name__ == "__main__":
    if not config.read('config.ini'):
        print("Could not find config file.")
        exit()
    app = web.Application()
    app.add_routes(routes)

    web.run_app(app, port=7400)
