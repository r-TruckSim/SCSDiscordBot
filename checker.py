import logging
import os
import sqlite3

import aiohttp
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


class URLChecker:

  def __init__(self, url, db_name):
    self.url = url
    self.conn = sqlite3.connect(db_name, check_same_thread=False)
    self.cursor = self.conn.cursor()
    self._create_table()

  def _create_table(self):
    """Creates a table for storing URLs"""
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                             (url text UNIQUE)''')
    self.conn.commit()

  async def handle_all_post_urls(self, client):
    """Gets all URLs which lead to blog posts and sends them"""
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(self.url) as response:
          html = await response.text()
    except Exception as e:
      logging.error(f'Failed to fetch URL: {e}')
      return
    soup = BeautifulSoup(html, 'html.parser')

    h3s = soup.find_all('h3', {'class': 'post-title entry-title'})
    new_urls = {h3.find('a')['href']: h3.find('a').text for h3 in h3s}

    for url, title in new_urls.items():
      success = self._add_url_to_db(url)
      if success:
        ecs_channel = client.get_channel(int(os.environ['ECS_CHANNEL_ID']))
        ecs_message = f"** :newspaper: | {title}**\n\n{url}"

        pm_channel = client.get_channel(int(os.environ['PM_CHANNEL_ID']))
        pm_message = f"** :newspaper: | {title}**\n\n{url}\n\n<@&{int(os.environ['ROLE_ID'])}>"

        logging.info(f'Sending message {ecs_message} to {ecs_channel}')
        logging.info(f'Sending message {pm_message} to {pm_channel}')

        await ecs_channel.send(ecs_message)
        await pm_channel.send(pm_message)

  def _add_url_to_db(self, url):
    """Tries to add URL to DB, fails if it exists"""
    try:
      self.cursor.execute("INSERT INTO urls VALUES (?)", (url, ))
      self.conn.commit()
      logging.info(f'Adding URL to DB: {url}')
      return True
    except sqlite3.IntegrityError as e:
      return False
