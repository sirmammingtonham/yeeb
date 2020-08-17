import sys
sys.path.append("../discord.py/")
import discord
from discord.ext import commands


with open("token.txt", "r") as f:
    TOKEN = f.read()
bot = commands.Bot(command_prefix = 'bruh ')
bot.remove_command('help')

extensions = ['bruh', 'music', 'events', 'card', 'speech']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
    bot.run(TOKEN)
