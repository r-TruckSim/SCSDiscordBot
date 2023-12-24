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

Set the following environment variables: 
* ```DISCORD_TOKEN``` - for Discord bot which sends messages
*  ```CHANNEL_ID``` - Discord channel where to send messages

Host the code and run it as long as you want.
