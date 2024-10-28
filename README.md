# Szefito Bot

**Version**: 1.1 (RC)  
**Date**: October 27th, 2024  
**Author**: Lucas V. Sobral, Brazil  

## Overview

Szefito Bot is a Discord bot designed for IP analysis using the ProxyCheck.io API. It allows users to verify if an IP address is a proxy, VPN, or business-related address, making it useful for managing secure environments or handling suspicious activity.

## Features

- **IP Address Check**: Use `!szefito checkproxy <IP_Address>` to analyze if an IP is associated with a proxy, VPN, or business entity.
- **Help Command**: Access detailed help using `!szefito help` or specific help for a command, like `!szefito help checkproxy`.
- **Info Command**: Provides information about the bot, its creator, and includes a motivational message.
- **CSV File Handling**: Szefito Bot can handle CSV files with IP addresses sent in DMs, analyzing them for proxy or VPN presence and sending back organized responses.
- **Privacy**: Szefito Bot only uses data from ProxyCheck.io's API without storing any user data. See the privacy policy for more details.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-repo/szefito-bot.git
   cd szefito-bot
   ```

2. Install required dependencies:

   ```bash
   pip install discord requests
   ```

3. Replace the `TOKEN` in `main.py` with your bot's actual token.

4. Run Requirements.txt
   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. Run the bot:

   ```bash
   python3 main.py
   ```

## Usage

- **Prefix**: The bot uses `!szefito` as a prefix for all commands.

### Commands

- **Check Proxy**:  
  `!szefito checkproxy <IP_Address>`  
  Checks if the provided IP address is a proxy, VPN, or business IP.

- **Info**:  
  `!szefito info`  
  Displays bot information and a motivational message.

- **Help**:  
  `!szefito help`  
  Provides an overview of all commands. Use `!szefito help <command>` for command-specific help.

### Handling CSV Files in DMs

Szefito Bot can receive a CSV file via DM in the format:

```
ip_address;usernames;last_use_unix;last_use
```

The bot will analyze each IP in the file and respond with proxy and region details.

## Privacy Policy

Szefito Bot respects user privacy, only accessing public data provided by ProxyCheck.io's API. You can view ProxyCheck.io's privacy policy [here](https://proxycheck.io/privacy). No private user data is stored or accessed by Szefito Bot. By using Szefito Bot, you agree to this policy.

---

This bot was created with the intent to make IP analysis accessible while respecting user privacy. Enjoy using Szefito Bot, and feel free to contribute or suggest new features!

--- 

hosted by eisberg, thanks an lot
ideas:szefito, jpx13 and panda

if you want use without hosting, here are the link how to use
https://discord.gg/FHhvkRvgMH
