# new world discord bot

Automated discord bot for displaying patch notes and checking server status from New World game.


![alt text](https://upload.wikimedia.org/wikipedia/en/b/bb/New_World_Cover_art.jpg)

## Requirements

- Python 3.8 and up - https://www.python.org/downloads/
- git - https://git-scm.com/download/

### How to install modules

```
for windows:
python -m pip install -r requirements.txt

for linux:
python3 -m pip install -r requirements.txt
```

### ENV

rename `.env.example` to `.env` then store your token and some other private info like this:

```
DISCORD_TOKEN=
discord_channel_webhook=
```

### PM2

PM2 is an alternative script provided by NodeJS, which will reboot your bot whenever it crashes and keep it up with a nice status. You can install it by doing `npm install -g pm2` and you should be done.

```
# Start the bot
pm2 start pm2.json

# Tips on common commands
pm2 <command> [name]
  start discordbot.py    Run the bot again if it's offline
  list                    Get a full list of all available services
  stop discordbot.py     Stop the bot
  reboot discordbot.py   Reboot the bot
```
