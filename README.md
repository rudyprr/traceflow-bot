# TraceFlow Discord Bot

A simple Discord bot that analyzes IP addresses and displays detailed information using the **TraceFlow API**.

## Features
- Slash command `/ip-details`
- IP address validation
- Country, city, timezone, ISP, and GPS coordinates
- Google Maps location link
- Clean and readable Discord embed

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

Use the command in Discord:
```bash
/ip-details <ip_address>
```

## API
Data is provided by traceflow.me
https://traceflow.me

