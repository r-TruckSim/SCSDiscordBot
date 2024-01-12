# SCSDiscordBot

 Discord bot for sending notifications about new posts in SCS Software blog.

## Major library dependencies

* discord-py
* beautifulsoup4

## Features

* HTML parsing - extraction of links inside tags
* Local DB - putting links and checking if they already exist
* Discord integration - sending messages with links to new blog posts

## Setup

Register the Discord bot.
Your bot should have server members intent to get user and send DM to them.

Set the following environment variables:

* ```DISCORD_TOKEN``` - for Discord bot which sends messages
* ```CHANNEL_ID``` - Discord channel where to send messages (currently it is being used multiple times, prefixed by server name)
* ```ROLE_ID``` - Role to ping when new blog post arrives
* ```USER_ID``` - User to send DM to if URL retrieval is unsuccessful

Host the code and run it as long as you want.
