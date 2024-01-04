import asyncio
import os
from threading import Thread

from discord import Client, Intents

from checker import URLChecker
from serv import app


class MyClient(Client):

  async def on_ready(self):
    """Starts up bot and creates scheduled async task"""
    print(f'Logged on as {self.user}!')
    self.loop.create_task(run_schedule())


async def run_schedule():
  """Runs URL checking on schedule"""
  while True:
    await checker.handle_all_post_urls(client)
    await asyncio.sleep(77)


URL = 'https://blog.scssoft.com/'
checker = URLChecker(URL, 'urls.db')

intents = Intents.default()
client = MyClient(intents=intents)

Thread(target=lambda: app.run(host="0.0.0.0")).start()
client.run(os.environ['DISCORD_TOKEN'])
