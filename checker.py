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
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
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
        if url_list is None:
            logging.error("URL list is empty, message won't be sent!")
            return

        for url, title in url_list.items():
            success = self._add_url_to_db(url)
            if success:
                ecs_channel = client.get_channel(int(os.environ["ECS_CHANNEL_ID"]))
                ecs_message = f"** :newspaper: | {title}**\n\n{url}"

                pm_channel = client.get_channel(int(os.environ["PM_CHANNEL_ID"]))
                pm_message = f"** :newspaper: | {title}**\n\n{url}\n\n<@&{int(os.environ['ROLE_ID'])}>"

                logging.info("Sending message %s to %s", ecs_message, ecs_channel)
                logging.info("Sending message %s to %s", pm_message, pm_channel)

                await ecs_channel.send(ecs_message)

                pm_sent_msg = await pm_channel.send(pm_message)
                await pm_sent_msg.publish()

    def _add_url_to_db(self, url: str):
        """Tries to add URL to DB, fails if it exists"""
        try:
            self.cursor.execute("INSERT INTO urls VALUES (?)", (url,))
            self.conn.commit()
            logging.info("Adding URL to DB: %s", url)
            return True
        except sqlite3.IntegrityError:
            return False
