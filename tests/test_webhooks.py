import json
import os
import unittest
from unittest.mock import AsyncMock

import aiohttp
import discord

import gitlab_discord_webhook.__main__ as main
from gitlab_discord_webhook.models import IssueHookPayload, PushHookPayload


def _load_json(file_name):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources", file_name)) as f:
        return json.load(f)


class TestWebhooks(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = aiohttp.ClientSession()

    async def asyncTearDown(self):
        await self.session.close()

    async def test_process_push_hook_new_commits(self):
        data = _load_json("push_commit.json")
        push = PushHookPayload.model_validate(data)

        main.send_message = AsyncMock()

        await main.process_push_hook(AsyncMock(), push)

        main.send_message.assert_called_once()
        embed = main.send_message.call_args[1]["embed"]
        self.assertIsInstance(embed, discord.Embed)


    async def test_process_issue_hook_new_issue(self):
        data = _load_json("issue_new.json")
        push = IssueHookPayload.model_validate(data)

        main.send_message = AsyncMock()

        await main.process_issue_hook(AsyncMock(), push)

        main.send_message.assert_called_once()
        embed = main.send_message.call_args[1]["embed"]
        self.assertIsInstance(embed, discord.Embed)
