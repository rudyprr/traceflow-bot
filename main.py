import discord
from discord.ext import commands
import aiohttp
from dotenv import load_dotenv
import json
import re
import os

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# IP Regex for validation
IP_REGEX = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')

    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="traceflow.me"
    )
    await bot.change_presence(activity=activity)

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name="ip-details", description="Analyze an IP address and get detailed information")
async def ip_details(interaction: discord.Interaction, ip_address: str):
    if not IP_REGEX.match(ip_address):
        embed = discord.Embed(
            title="❌ Error",
            description="The provided IP address is not valid.",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    embed_loading = discord.Embed(
        title="🔍 Analyzing...",
        description=f"Fetching information for IP: `{ip_address}`",
        color=0xffaa00
    )
    await interaction.response.send_message(embed=embed_loading)
    
    try:
        # TraceFlow API request
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.traceflow.me/ip-details/{ip_address}') as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Color based on IP type
                    embed_color = 0x4285f4  

                    # Embed creation
                    embed = discord.Embed(
                        color=embed_color
                    )

                    embed.set_author(
                        name=f"TraceFlow : {data.get('ip', 'N/A')}",
                        icon_url="https://traceflow.me/img/logo/icon.png",
                        url=f"https://traceflow.me/ip-details?ip={data.get('ip', 'N/A')}"
                    )
                    
                    # Hostname
                    if data.get('hostname'):
                        embed.add_field(
                            name="Hostname",
                            value=f"**`{data['hostname']}`**",
                            inline=False
                        )

                    # Country and Organization
                    if data.get('country'):
                        embed.add_field(
                            name="Country",
                            value=f"{data['country']}",
                            inline=True
                        )
                    if data.get('org'):

                        embed.add_field(
                            name="Organization",
                            value=f"{data['org']}",
                            inline=True
                        )
                    
                    if data.get('country') and data.get('org'):
                        embed.add_field(name="\u200b", value="\u200b", inline=True)


                    # City and time zone
                    if data.get('city'):
                        embed.add_field(
                            name="City",
                            value=data['city'] if data['city'] else "*N/A*",
                            inline=True
                        )
                    if data.get('timezone'):
                        embed.add_field(
                            name="Timezone",
                            value=f"{data['timezone']}",
                            inline=True
                        )
                    
                    if (data.get('city') or data.get('region')) and data.get('timezone'):
                        embed.add_field(name="\u200b", value="\u200b", inline=True)


                    # Region and postal code
                    if data.get('region'):
                        embed.add_field(
                            name="Region",
                            value=data['region'] if data['region'] else "*N/A*",
                            inline=True
                        )
                    if data.get('postal'):
                        embed.add_field(
                            name="Postal Code",
                            value=data['postal'] if data['postal'] else "*N/A*",
                            inline=True
                        )
                    
                    if data.get('region') or data.get('postal'):
                        embed.add_field(name="\u200b", value="\u200b", inline=True)


                    if data.get('loc'):
                        embed.add_field(name="---", value="\u200b", inline=False)

                    if data.get('loc'):
                        coords = data['loc'].split(',')
                        if len(coords) == 2:
                            lat, lon = coords
                            
                            # GPS Coordinates
                            embed.add_field(
                                name="🛰️ GPS Coordinates",
                                value=f"**Latitude:** `{lat}`\n**Longitude:** `{lon}`",
                                inline=True
                            )
                            
                            # Google Maps Link
                            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                            embed.add_field(
                                name="📍 View on Map",
                                value=f"[Click Here to View]({maps_url})",
                                inline=True 
                            )
                    
                    embed.set_footer(
                        text=f"Data provided by traceflow.me",
                    )

                
                elif response.status == 404:
                    embed = discord.Embed(
                        title="❌ IP Not Found",
                        description=f"No information available for IP: `{ip_address}`",
                        color=0xff6600
                    )
                
                else:
                    embed = discord.Embed(
                        title="⚠️ API Error",
                        description=f"Error {response.status}: Unable to retrieve information.",
                        color=0xff0000
                    )
    
    except aiohttp.ClientError as e:
        embed = discord.Embed(
            title="🔌 Connection Error",
            description="Unable to connect to TraceFlow API.",
            color=0xff0000
        )
    except json.JSONDecodeError:
        embed = discord.Embed(
            title="📄 Data Error",
            description="Invalid response from API.",
            color=0xff0000
        )
    except Exception as e:
        embed = discord.Embed(
            title="💥 Unexpected Error",
            description=f"An error occurred",
            color=0xff0000
        )
    
    # Update message with results
    await interaction.edit_original_response(embed=embed)

# Global error handler for slash commands
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    embed = discord.Embed(
        title="❌ Command Error",
        description="An error occurred while executing the command.",
        color=0xff0000
    )
    
    if not interaction.response.is_done():
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.followup.send(embed=embed, ephemeral=True)

# Entry point
if __name__ == "__main__":
    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    
    print("Starting TraceFlow Bot...")
    
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Invalid Discord token!")
    except Exception as e:
        print(f"Startup error: {e}")