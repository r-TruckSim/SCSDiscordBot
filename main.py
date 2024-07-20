import argparse
import asyncio
import os
import logging

from discord import Client, Intents
from checker import URLChecker

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Discord Bot to send messages and check URLs.")
parser.add_argument('--channel_id', type=str, help='The ID of the channel to send the message to.')
parser.add_argument('--message', type=str, help='The message content to send.')
args = parser.parse_args()

class MyClient(Client):
    """Discord client"""

    async def on_ready(self):
        """Starts up bot and creates scheduled async task"""
        logging.info("Logged on as %s!", self.user)

        if args.channel_id and args.message:
            await send_custom_message(args.channel_id, args.message)
        else:
            self.loop.create_task(run_schedule())

async def send_custom_message(channel_id, message):
    """Send custom message via CLI"""
    channel = client.get_channel(int(channel_id))
    if channel:
        await channel.send(message)
        logging.info("Sent custom message to channel %s: %s", channel_id, message)
    else:
        logging.error("Channel with ID %s not found.", channel_id)

async def run_schedule():
    """Runs URL checking on schedule"""
    while True:
        try:
            urls = await checker.get_all_post_urls(client)
            await checker.send_msgs_to_channels(client, urls)
        except Exception as e:
            logging.error("Exception occurred: %s", e)
            await asyncio.sleep(77)
        finally:
            await asyncio.sleep(77)


URL = "https://blog.scssoft.com/"
checker = URLChecker(URL, "urls.db")

intents = Intents.default()
intents.members = True
client = MyClient(intents=intents)

client.run(os.environ["DISCORD_TOKEN"])
