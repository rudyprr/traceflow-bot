# TraceFlow Discord Bot

A simple Discord bot that analyzes IP addresses and displays detailed information using the **TraceFlow API**.

#### [Invite the bot](https://top.gg/bot/1377253418183426069) to your server.

## Features
- Slash command `/ip-details`
- Country, city, timezone, ISP, and GPS coordinates
- Google Maps location link

<img width="379" height="424" alt="Screenshot 2025-12-17 210245" src="https://github.com/user-attachments/assets/d0bd8df3-97f2-4d1e-bff2-1c638f2f4a03" />

## Requirements
- Python 3.9+
- A Discord Bot Token

## Installation
```bash
git clone https://github.com/rudyprr/traceflow-bot.git
cd traceflow-bot
pip install -r requirements.txt
```

## Configuration
Create a .env file and add:
```bash
TOKEN=your_discord_bot_token_here
```

## Usage
```bash
python main.py
```

## Use the command in Discord:
```bash
/ip-details <ip_address>
```

## API
Data is provided by traceflow.me
https://traceflow.me

