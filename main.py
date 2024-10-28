import discord
import requests
import csv
from discord.ext import commands

# Replace TOKEN with your actual token
TOKEN = 'your-discord-bot-token'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!szefito ', intents=intents)

@bot.command()
async def checkproxy(ctx, ip_address: str):
    url = f"https://proxycheck.io/v2/{ip_address}?vpn=1&asn=1"
    response = requests.get(url).json()
    
    if response['status'] == "ok":
        ip_info = response[ip_address]
        is_proxy = "Yes" if ip_info['proxy'] == "yes" else "No"
        response_msg = (
            f"**IP Address**: {ip_address}\n"
            f"**Provider**: {ip_info['provider']}\n"
            f"**Country**: {ip_info['country']}\n"
            f"**Proxy**: {is_proxy}\n"
            f"**Type**: {ip_info['type']}\n"
        )
        await ctx.send(response_msg)
    else:
        await ctx.send("Failed to retrieve data from proxycheck.io.")

@bot.command()
async def info(ctx):
    await ctx.send(
        "This bot was created by Szefito, Brazil. "
        "Keep pushing forward, you are capable of great things!"
      
        "thanks to eisberg for host and help, ideas help from:szefito,jpx13 and panda
    )

@bot.command(name='helpme')
async def szefito_help(ctx, *args):
    if len(args) == 0:
        help_message = """
        **Szefito Bot Help:**

        **Commands:**
        - **checkproxy <IP_Address>**:  
          Check if the provided IP address is a proxy, VPN, or associated with any businesses.  
          **Usage**: `!szefito checkproxy <IP_Address>`

        - **info**:  
          Get information about the bot, its creator, and a motivational phrase.  
          **Usage**: `!szefito info`

        - **help**:  
          Display this help message, providing details on all available commands. You can also get more information on a specific command.  
          **Usage**:  
            - General help: `!szefito help`  
            - Command-specific help: `!szefito help checkproxy`

        **How it works**:  
        The bot uses the command prefix `!szefito`, followed by the command name and any necessary parameters. It processes proxy checks for IP addresses, gives bot information, and provides more through simple commands.

        **Examples:**
        - To check if an IP is a proxy: `!szefito checkproxy 177.37.148.151`
        - To get info about the bot: `!szefito info`

        You can type `!szefito help <command>` to get more specific help for each command.
        """
        await ctx.send(help_message)
    else:
        command = args[0]
        if command == 'checkproxy':
            await ctx.send("""
            **checkproxy <IP_Address>**:  
            Check if the provided IP address is a proxy, VPN, or associated with any businesses.  
            **Usage**: `!szefito checkproxy 177.37.148.151`
            """)
        elif command == 'info':
            await ctx.send("""
            **info**:  
            Get information about the bot, its creator (Szefito, Brazil), and a motivational phrase.  
            **Usage**: `!szefito info`
            """)
        else:
            await ctx.send(f"Unknown command `{command}`. Type `!szefito help` for available commands.")

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) or message.guild is None:
        if message.attachments and message.attachments[0].filename.endswith('.csv'):
            attachment = message.attachments[0]

            processing_message = await message.channel.send("Processing IP addresses, please wait...")

            csv_content = await attachment.read()
            csv_text = csv_content.decode('utf-8').splitlines()
            csv_reader = csv.reader(csv_text, delimiter=';')
            results = []

            for row in csv_reader:
                ip_address = row[0]
                url = f"https://proxycheck.io/v2/{ip_address}?vpn=1&asn=1"
                response = requests.get(url).json()
                
                if response['status'] == "ok":
                    ip_info = response[ip_address]
                    is_proxy = "Yes" if ip_info['proxy'] == "yes" else "No"
                    city = ip_info.get('city', 'Unknown')
                    country = ip_info.get('country', 'Unknown')
                    provider = ip_info.get('provider', 'Unknown')
                    result = (
                        f"**IP**: {ip_address}\n"
                        f"  • **Proxy**: {is_proxy}\n"
                        f"  • **Type**: {ip_info.get('type', 'N/A')}\n"
                        f"  • **City**: {city}, **Country**: {country}\n"
                        f"  • **Provider**: {provider}\n"
                    )
                    results.append(result)

            message_content = "\n\n".join(results)

            if len(message_content) > 2000:
                chunks = [message_content[i:i+2000] for i in range(0, len(message_content), 2000)]
                await processing_message.edit(content="We got a reply! Here are the results:")
                for chunk in chunks:
                    await message.channel.send(chunk)
            else:
                await processing_message.edit(content=f"We got a reply! Here are the results:\n{message_content}")

    await bot.process_commands(message)

bot.run(TOKEN)
