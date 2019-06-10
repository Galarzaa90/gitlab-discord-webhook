import configparser

import aiohttp
import discord
from aiohttp import web

config = configparser.ConfigParser()
if not config.read('config.ini'):
    print("Could not find config file.")
    exit()

routes = web.RouteTableDef()


@routes.post('/webhook/gitlab')
async def receive_webhook(request: web.Request):
    try:
        event_type = request.headers.getone('x-gitlab-event')
    except KeyError:
        return web.HTTPBadRequest(text="GitLab event type not found.")
    body = await request.json()
    if event_type == "Push Hook":
        await process_push_hook(body)
    if event_type == "Issue Hook":
        await process_issue_hook(body)
    if event_type == "Note Hook":
        await process_note_hook(body)
    if event_type == "Merge Request Hook":
        await process_merge_request_hook(body)
    return web.Response(text="OK")


async def process_push_hook(data):
    """Builds and sends an embed message with new commits information."""
    repository = data["repository"]
    commit_count = data["total_commits_count"]
    branch = data["ref"].replace("refs/heads/", "")
    commit_str = "commit" if commit_count == 1 else "commits"
    # Show link to commit compare if there's more than one commit
    if commit_count > 1:
        embed_url = f"{repository['homepage']}/compare/{data['before'][:7]}...{data['after'][:7]}"
    else:
        embed_url = f"{repository['homepage']}/commit/{data['after'][:7]}"

    embed = discord.Embed(title=f"[{repository['name']}:{branch}] {commit_count} new {commit_str}", url=embed_url,
                          colour=discord.Colour.blurple())
    embed.set_author(name=data["user_username"], icon_url=data["user_avatar"])
    embed.description = ""
    for commit in data["commits"]:
        message = commit["message"].splitlines()[0]
        embed.description += f"[`{commit['id'][:7]}`]({commit['url']}) {message} - {commit['author']['name']}\n"
    await send_message(None, embed=embed)


async def process_issue_hook(data):
    """Builds and sends an embed message with issues information."""
    repository = data["repository"]
    issue = data["object_attributes"]
    user = data["user"]
    description = ""
    action = "Issue updated"
    colour = discord.Colour.light_grey()
    if issue["action"] == "open":
        action = "Issue opened"
        description = issue['description']
        colour = discord.Colour.green()
    elif issue["action"] == "close":
        action = "Issue closed"
        colour = discord.Colour.dark_grey()
    embed = discord.Embed(title=f"[{repository['name']}] {action}: #{issue['iid']} {issue['title']}"
                          , url=issue["url"], description=description, colour=colour)
    embed.set_author(name=user["username"], icon_url=user["avatar_url"])
    await send_message(None, embed=embed)


async def process_note_hook(data):
    """Builds and sends an embed message with notes information."""
    repository = data["repository"]
    note = data["object_attributes"]
    user = data["user"]
    colour = discord.Colour.greyple()
    embed = discord.Embed(url=note["url"], description=note["note"], colour=colour)
    embed.set_author(name=user["username"], icon_url=user["avatar_url"])
    if "issue" in data:
        issue = data["issue"]
        embed.title = f"[{repository['name']}] New comment on issue #{issue['iid']}: {issue['title']}"
    if "commit" in data:
        commit = data["commit"]
        embed.title = f"[{repository['name']}] New comment on commit `{commit['id'][:7]}`"
    if "merge_request" in data:
        merge = data["merge_request"]
        embed.title = f"[{repository['name']}] New comment on merge request !{merge['iid']}: {merge['title']}"
    await send_message(None, embed=embed)


async def process_merge_request_hook(data):
    """Builds and sends an embed message with merge request information."""
    repository = data["repository"]
    merge = data["object_attributes"]
    user = data["user"]
    description = ""
    action = "Issue updated"
    colour = discord.Colour.light_grey()
    if merge["action"] == "open":
        action = "Merge request opened"
        description = merge['description']
        colour = discord.Colour.dark_green()
    elif merge["action"] == "close":
        action = "Merge request closed"
        colour = discord.Colour.dark_grey()
    embed = discord.Embed(title=f"[{repository['name']}] {action}: !{merge['iid']} {merge['title']}"
                          , url=merge["url"], description=description, colour=colour)
    embed.set_author(name=user["username"], icon_url=user["avatar_url"])
    embed.set_footer(text=f"{merge['source_branch']} → {merge['target_branch']}")
    await send_message(None, embed=embed)


async def send_message(content, **kwargs):
    async with aiohttp.ClientSession() as session:
        try:
            webhook = discord.Webhook.from_url(config['Discord']['webhook'],
                                               adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(content, **kwargs)
        except Exception as e:
            web.HTTPInternalServerError(text=str(e))


app = web.Application()
app.add_routes(routes)

web.run_app(app, port=7400)
