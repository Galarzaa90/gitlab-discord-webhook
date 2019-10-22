import json
import os
import asynctest
import discord

import main
import models


def _load_json(file_name):
    with open(os.path.join("resources", file_name)) as f:
        return json.load(f)


class TestWebhooks(asynctest.TestCase):

    async def test_process_push_hook_new_commits(self):
        data = _load_json("push_commit.json")
        push = models.PushRequest(**data)

        main.send_message = asynctest.CoroutineMock()

        await main.process_push_hook(push)

        main.send_message.assert_called_once()
        embed = main.send_message.call_args[1]["embed"]
        self.assertIsInstance(embed, discord.Embed)

