import sys
sys.path.append("../discord.py/")
import discord
from discord.ext import commands


with open("token.txt", "r") as f:
    TOKEN = f.read()
bot = commands.Bot(command_prefix = 'bruh ')
bot.remove_command('help')

# status = ['Minecraft', 'Roblox', 'Fortnite', 'on split screen']
extensions = ['bruh', 'music', 'events', 'card', 'speech']
# extensions = ['speech']

if __name__ == '__main__':
    for extension in extensions:
        # try:
        bot.load_extension(extension)
        # except Exception as e:
        #     print(f'{extension} cannot be loaded. [{e}]')
    bot.run(TOKEN)
