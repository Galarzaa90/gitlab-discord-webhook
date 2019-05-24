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

    embed = discord.Embed(title=f"[{repository['name']}:{branch}] {commit_count} new {commit_str}", url=embed_url)
    embed.set_author(name=data["user_name"], icon_url=data["user_avatar"])
    embed.description = ""
    for commit in data["commits"]:
        message = commit["message"].splitlines()[0]
        embed.description += f"[`{commit['id'][:7]}`]({commit['url']}) {message} - {commit['author']['name']}\n"
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
