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

## Hosting VM
1. git clone https://github.com/r-TruckSim/SCSDiscordBot
2. cd SCSDiscordBot
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. sudo nano /etc/systemd/system/scsbot.service
7. Enter this into your file

```
[Unit]
Description=SCS Discord Bot
After=network.target

[Service]
User=yourusername
WorkingDirectory=/home/yourusername/SCSDiscordBot
Environment="DISCORD_TOKEN=your_token"
Environment="CHANNEL_ID=123456789"
Environment="ROLE_ID=987654321"
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

8. sudo systemctl daemon-reload
9. sudo systemctl enable scsbot
10. sudo systemctl start scsbot
11. sudo systemctl status scsbot
12. Bot will run 24/7 and auto restart
