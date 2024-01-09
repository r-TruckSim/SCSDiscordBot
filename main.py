import asyncio
import os
import logging

from discord import Client, Intents

from checker import URLChecker

logging.basicConfig(level=logging.INFO)


class MyClient(Client):
    """Discord client"""

    async def on_ready(self):
        """Starts up bot and creates scheduled async task"""
        logging.info(f"Logged on as {self.user}!")
        self.loop.create_task(run_schedule())


async def run_schedule():
    """Runs URL checking on schedule"""
    while True:
        urls = await checker.get_all_post_urls(client)
        await checker.send_msgs_to_channels(client, urls)
        await asyncio.sleep(77)


URL = "https://blog.scssoft.com/"
checker = URLChecker(URL, "urls.db")

intents = Intents.default()
client = MyClient(intents=intents)

client.run(os.environ["DISCORD_TOKEN"])
