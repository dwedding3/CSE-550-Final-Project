# Butler Bot
# Main.py
# Glue code for all Butler Bot code

import discord
import os
import json
import sys
from discord.ext import commands

from InitializeConfig import startInit

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print("Bot Online")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')
     
#command that sends back list of all available cogs that Admins can load and unload
@bot.command(description = "lists available cogs")
async def list_cogs(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await ctx.send(f'{filename[:-3]}')
            
#loads all cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        
config = startInit()

bot.run(config['token'])

print("shutdown complete")