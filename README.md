# Discord Crypto Faucet Bot

> A basic discord bot made with discord.py

## Requirements

- Python 3.9.x
- Pip
- Virtualenv
- PM2 (optional)

## Setup

1. Install python, pip and virtualenv if you haven't yet
2. Clone this repository with `git clone git@github.com:ItsANameToo/discord-faucet-bot.git`
3. Navigate to the folder `cd discord-faucet-bot`
4. Create a virtualenv by running `virtualenv -p python3 venv`
5. Activate the virtualenv `source venv/bin/activat`
6. Install requirements `pip install -r requirements.txt`
7. Setup your `.env` , don't forget to create a bot token, see https://discord.com/developers/docs/topics/oauth2
8. Run the script to bring your bot to life `python main.py`
9. Invite your bot to the discord of your liking. It only needs permissions to read/write to channels, no administrative permissions required

## Server

For running it on the server with pm2, run the following:

```bash
source venv/bin/activate
pm2 start main.py --name arkbot --interpreter python3
```

This allows you to easily start/stop/restart the bot
