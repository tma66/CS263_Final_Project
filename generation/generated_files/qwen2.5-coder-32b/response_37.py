import discord
from discord.ext import commands
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create an instance of a bot
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    logging.info(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello! How can I help you today?')

@bot.command()
async def upload(ctx, *, filename: str):
    try:
        with open(filename, 'rb') as file:
            await ctx.send(file=discord.File(file))
    except FileNotFoundError:
        await ctx.send(f'File {filename} not found.')

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')