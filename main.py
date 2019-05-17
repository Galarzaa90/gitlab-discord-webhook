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
async def login(request: web.Request):
    try:
        event_type = request.headers.getone('x-gitlab-event')
    except KeyError:
        return web.HTTPBadRequest(text="GitLab event type not found.")
    body = await request.json()
    if event_type == "Push Hook":
        await process_push_hook(body)
    return web.Response(text="OK")


async def process_push_hook(data):
    repository = data["repository"]
    commit_count = data["total_commits_count"]

    embed = discord.Embed(title=f"[{repository['name']}] {commit_count} new commits", url=repository['homepage'])
    embed.set_author(name=data["user_name"], icon_url=data["user_avatar"])
    embed.description = ""
    for commit in data["commits"]:
        embed.description += f"[`{commit['id'][:7]}`]({commit['url']}) {commit['message']} - {commit['author']['name']}\n"
    await send_message(None, embed=embed)


async def send_message(content, **kwargs):
    async with aiohttp.ClientSession() as session:
        try:
            webhook = discord.Webhook.from_url(config['Discord']['webhook'], adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(content, **kwargs)
        except Exception as e:
            web.HTTPInternalServerError(text=str(e))


app = web.Application()
app.add_routes(routes)

web.run_app(app, port=7400)
