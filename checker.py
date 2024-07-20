import logging
import os
import sqlite3

import aiohttp
from bs4 import BeautifulSoup
from discord import Client

logging.basicConfig(level=logging.INFO)


class URLChecker:
    """Checking blog posts on specific URL"""

    def __init__(self, url, db_name):
        self.url = url
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Creates a table for storing URLs"""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS urls
                             (url text UNIQUE)"""
        )
        self.conn.commit()

    async def get_all_post_urls(self, client: Client) -> dict:
        """Gets all URLs which lead to blog posts.
           Sends DM to user if URL retrieval is not successful"""
        try:
            async with aiohttp.ClientSession() as session, session.get(self.url) as response:
                html = await response.text()

                logging.info("Successfully connected to %s", self.url)
                logging.info("Currently logged on as %s", client.user)
        except Exception as e:
            error_str = "Failed to fetch URL: %s", repr(e)
            logging.error(error_str)

            user = client.get_user(int(os.environ["USER_ID"]))
            await user.send(error_str)
            return

        soup = BeautifulSoup(html, "html.parser")

        h3s = soup.find_all("h3", {"class": "post-title entry-title"})
        new_urls = {h3.find("a")["href"]: h3.find("a").text for h3 in h3s}

        return new_urls

    async def send_msgs_to_channels(self, client: Client, url_list: dict):
        """Send messages with blog posts to Discord channels"""

        async def send_message(channel_id, message, role_id=None):
            channel = client.get_channel(int(channel_id))
            sent_message = await channel.send(message)

            if role_id:
                await sent_message.publish()
                message += f"\n\n<@&{int(role_id)}>"

            logging.info("Sending message %s to %s", message, channel)
            return sent_message

        if not url_list:
            logging.error("URL list is empty, message won't be sent!")
            return

        ecs_channel_id = os.environ["ECS_CHANNEL_ID"]
        tsl_channel_id = os.environ["TSL_CHANNEL_ID"]
        pm_channel_id = os.environ["PM_CHANNEL_ID"]
        role_id = os.environ["ROLE_ID"]

        for url, title in url_list.items():
            if self._add_url_to_db(url):
                message = f"** :newspaper: | {title}**\n\n{url}"
                await send_message(ecs_channel_id, message)
                await send_message(tsl_channel_id, message)
                await send_message(pm_channel_id, message, role_id)

    def _add_url_to_db(self, url: str):
        """Tries to add URL to DB, fails if it exists"""
        try:
            self.cursor.execute("INSERT INTO urls VALUES (?)", (url,))
            self.conn.commit()
            logging.info("Adding URL to DB: %s", url)
            return True
        except sqlite3.IntegrityError:
            return False
