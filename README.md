# 🔍 Szefito Bot 2.0

**Version**: 2.0 | **Release Date**: February 06th, 2024  
**Developer**: Lucas V. Sobral (Brazil) | **Host**: Eisberg  
**Support Server**: [Join Discord](https://discord.gg/FHhvkRvgMH)

![Security Shield](https://img.shields.io/badge/Security-Level_2-green) 
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)

## 🌟 Overview
Advanced Discord bot for IP analysis leveraging ProxyCheck.io's API. Now with enhanced security and CSV processing capabilities!

---

## 🚀 Key Features
### 🔒 Security Enhancements
- End-to-end encrypted IP verification
- Token isolation in `.env` file
- Zero data storage policy
- Secure CSV processing via DMs

### ⚡ Core Functionality
- **Proxy/VPN Detection**: `!checkproxy <IP>`
- **Batch Processing**: Analyze CSV files via DM
- **Instant Help**: `!helpme <command>`
- **Bot Insights**: `!info` command

---

## 🛠️ Installation Guide
```bash
git clone https://github.com/lucassobralofc/szefitoiplooker.git
cd szefitoiplooker
python3 -m pip install -r requirements.txt
```

### Configuration
1. Create `.env` file:
```env
DISCORD_TOKEN=your_bot_token_here
```

2. **Never commit** `.env` to version control!

---

## 📋 Command Reference
| Command | Description | Example |
|---------|-------------|---------|
| `!checkproxy` | IP analysis | `!checkproxy 192.168.1.1` |
| `!info` | Bot details | `!info` |
| `!helpme` | Command help | `!helpme checkproxy` |

---

## 📁 CSV Processing
### DM the bot with CSV files containing:
```csv
ip_address;usernames;last_use_unix;last_use
```

### Output Format:
```
IP: 192.168.1.1
Proxy: Yes (VPN)
Organization: Example Corp
Region: North America
```

---

## 🔐 Privacy Policy
- Zero user data storage
- All data processed through ProxyCheck.io ([Privacy Policy](https://proxycheck.io/privacy))
- Full Discord system encryption

---

## 🙌 Credits & Acknowledgments
**Core Team**:  
- Szefito (Concept)  
- JPX13 (Concept)  
- Panda (Testing)  

**Special Thanks**:  
Eisberg for hosting support

---

## ❓ Support & Self-Hosting
[![Support Server](https://img.shields.io/discord/849576827627339776?label=Support%20Server&style=for-the-badge)](https://discord.gg/FHhvkRvgMH)

For self-hosting assistance, join our Discord community!
