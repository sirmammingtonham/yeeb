import os
import discord
import nltk
from src.bot import YeebBot

print('discord version', discord.__version__)
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

bot = YeebBot(command_prefix='bruh ', guild_subscriptions=True,
              intents=discord.Intents.all())

bot.lavalink_nodes = [
    {"host": "lavalink.tapori.xyz", "port": 8804,
        "password": "whyareyougay", "https": False},
    {"host": "lava1.cruzstudio.tech", "port": 80,
        "password": "cruzstudio.tech", "https": False},
    {"host": "lava2.cruzstudio.tech", "port": 80,
        "password": "cruzstudio.tech", "https": False},
]

if 'SPOTIFY_CLIENT' in os.environ:
    bot.spotify_credentials = {
        'client_id': os.getenv('SPOTIFY_CLIENT'),
        'client_secret': os.getenv('SPOTIFY_SECRET'),
    }

if __name__ == '__main__':
    bot.run(os.getenv('AUTH_TOKEN'))
