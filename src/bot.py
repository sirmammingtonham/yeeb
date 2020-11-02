import sys
sys.path.append("../discord.py/")
import discord
from discord.ext import commands

print('discord version', discord.__version__)

with open("../res/token.txt", "r") as f:
    TOKEN = f.read()
# Configure intents (1.5.0)
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = 'bruh', guild_subscriptions=True, intents=intents)
bot.remove_command('help')

extensions = ['bruh', 'music', 'events', 'card']  # 'speech'

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
    bot.run(TOKEN)
