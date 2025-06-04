import discord
from discord.ext import commands
import os
import logging

# Bot configuration
TOKEN = 'YOUR_BOT_TOKEN'

# Create a new bot instance
bot = commands.Bot(command_prefix='!')

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Event listener for when the bot is ready
@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

# Command to log a message in the console and Discord channel
@bot.command(name='log')
async def log(ctx, *, message):
    logger.info(f'User {ctx.author.name} sent: {message}')
    await ctx.send(f'I logged your message: {message}')

# Command to upload a file from the local directory
@bot.command(name='upload')
async def upload(ctx, filename: str = None):
    if not filename:
        return await ctx.send('Please specify a file name!')
    
    try:
        with open(filename, 'rb') as f:
            await ctx.send(file=discord.File(f))
    except FileNotFoundError:
        return await ctx.send(f'File {filename} not found!')

# Command to get the bot's latency
@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'My current latency is {latency}ms')

# Run the bot with your token
bot.run(TOKEN)