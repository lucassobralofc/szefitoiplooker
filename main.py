import discord
import requests
import csv
import os
import asyncio
import re
import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

IP_REGEX = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

def convert_unix_timestamp(timestamp_str):
    """Convert a Unix timestamp to a human-readable date."""
    try:
        timestamp = float(timestamp_str)
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError, OverflowError):
        return "Invalid timestamp"

def create_proxy_embed(ip_address, ip_info):
    """Create an embed for proxy check results."""
    embed = discord.Embed(
        title="Proxy Check Results",
        description=f"Information for IP: {ip_address}",
        color=0x00ff00 if ip_info.get('proxy') == 'no' else 0xff0000
    )
    
    # Safely get devices information
    devices = ip_info.get('devices', {})
    
    fields = [
        ("Provider", ip_info.get('provider', 'Unknown'), True),
        ("Country", ip_info.get('country', 'Unknown'), True),
        ("Proxy", "Yes" if ip_info.get('proxy') == 'yes' else "No", True),
        ("Type", ip_info.get('type', 'N/A'), True),
        ("City", ip_info.get('city', 'Unknown'), True),
        ("ASN", ip_info.get('asn', 'Unknown'), True),
        ("Hostname", ip_info.get('hostname', 'Unknown'), True),
        ("Devices", f"Address: {devices.get('address', 'N/A')}\nSubnet: {devices.get('subnet', 'N/A')}", True),  # Added devices
        ("Risk", str(ip_info.get('risk', 'N/A')), True)
    ]
    
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    
    return embed

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def checkproxy(ctx, ip_address: str):
    """Check if an IP address is a proxy/VPN."""
    if not re.match(IP_REGEX, ip_address):
        await ctx.send("Invalid IP address format. Please use x.x.x.x format.")
        return

    try:
        response = requests.get(
            f"https://proxycheck.io/v2/{ip_address}?vpn=1&asn=1",
            timeout=10
        ).json()
    except Exception as e:
        await ctx.send(f"Error accessing proxycheck.io: {str(e)}")
        return

    if response.get('status') == "ok":
        ip_info = response.get(ip_address, {})
        embed = create_proxy_embed(ip_address, ip_info)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to retrieve data from proxycheck.io. The IP might be invalid or the service is unavailable.")

@bot.command()
async def info(ctx):
    """Show bot information."""
    embed = discord.Embed(
        title="Szefito Bot Information",
        description="https://x.com/takszefito/status/1884409675677868526",
        color=0x7289DA
    )
    embed.add_field(name="Creator", value="Szefito, Brazil", inline=False)
    embed.add_field(name="Version", value="2.3.1 (API Update, Please Verify GitHub!)", inline=False)
    embed.add_field(name="Source", value="https://github.com/lucassobralofc/szefitoiplooker/", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='helpme')
async def szefito_help(ctx, command_name: str = None):
    """Show help information."""
    if not command_name:
        embed = discord.Embed(
            title="Szefito Bot Help",
            description="Command prefix: `!`\nUse `!helpme <command>` for detailed help",
            color=0x7289DA
        )
        
        commands_info = {
            'checkproxy': 'Check if an IP is a proxy/VPN',
            'info': 'Show bot information',
            'helpme': 'Show this help message'
        }
        
        for cmd, desc in commands_info.items():
            embed.add_field(name=f"!{cmd}", value=desc, inline=False)
        
        embed.set_footer(text="Support:lucassobralofc@mail.com")
        await ctx.send(embed=embed)
    else:
        command = bot.get_command(command_name)
        if command:
            embed = discord.Embed(
                title=f"Help for !{command.name}",
                description=command.help,
                color=0x7289DA
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Command `{command_name}` not found.")

async def process_csv(file_content):
    """
    Process CSV content and return results.
    Expected CSV format: IP;username(s);last_use_unix;last_use_days
    """
    csv_text = file_content.decode('utf-8').splitlines()
    csv_reader = csv.reader(csv_text, delimiter=';')
    results = []
    
    for row_number, row in enumerate(csv_reader, 1):
        if not row or len(row) < 4:
            results.append(f"Row {row_number}: Invalid row format")
            continue
            
        try:
            ip_address = row[0].strip()
            usernames = row[1].strip()
            last_use_unix = row[2].strip()
            last_use_days = row[3].strip()
            
            if not re.match(IP_REGEX, ip_address):
                results.append(f"Row {row_number}: Invalid IP format")
                continue

            human_date = convert_unix_timestamp(last_use_unix)
            
            url = f"https://proxycheck.io/v2/{ip_address}?vpn=1&asn=1"
            response = requests.get(url, timeout=10).json()
            await asyncio.sleep(1)

            if response.get('status') == "ok":
                ip_info = response.get(ip_address, {})
                devices = ip_info.get('devices', {})
                
                result = (
                    f"IP: {ip_address}\n"
                    f"Usernames: {usernames}\n"
                    f"Last Used: {human_date} (Last Use Days: {last_use_days})\n"
                    f"Proxy: {'Yes' if ip_info.get('proxy') == 'yes' else 'No'} | "
                    f"Type: {ip_info.get('type', 'N/A')}\n"
                    f"Location: {ip_info.get('city', 'Unknown')}, {ip_info.get('country', 'Unknown')}\n"
                    f"Hostname: {ip_info.get('hostname', 'N/A')}\n"
                    f"Devices: Address={devices.get('address', 'N/A')}, Subnet={devices.get('subnet', 'N/A')}\n"  # Added devices
                    f"Provider: {ip_info.get('provider', 'Unknown')}\n"
                    f"{'-'*40}"
                )
                results.append(result)
            else:
                results.append(f"Row {row_number}: Failed to check IP {ip_address}")

        except Exception as e:
            results.append(f"Row {row_number}: Error processing - {str(e)}")
    
    return results

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.csv'):
                processing_msg = await message.channel.send("⏳ Processing CSV file... (This may take a few minutes)")
                
                try:
                    file_content = await attachment.read()
                    results = await process_csv(file_content)
                    
                    if not results:
                        await processing_msg.edit(content="❌ No valid data found in CSV file.")
                        return

                    with open('results.txt', 'w', encoding='utf-8') as f:
                        f.write('\n\n'.join(results))
                    
                    await message.channel.send(
                        content="✅ Processing complete! Here are your results:",
                        file=discord.File('results.txt')
                    )
                    await processing_msg.delete()
                    
                except Exception as e:
                    await message.channel.send(f"❌ Error processing file: {str(e)}")
                finally:
                    if os.path.exists('results.txt'):
                        os.remove('results.txt')

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Command is on cooldown. Try again in {error.retry_after:.1f} seconds.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing required argument. Use !helpme for command usage.")
    else:
        await ctx.send(f"❌ An error occurred, call Szefito!: {str(error)}")

if __name__ == "__main__":
    bot.run(TOKEN)