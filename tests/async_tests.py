import asyncio

import discord
from discord.ext import commands
# from discord.rtp import SilencePacket, RTPPacket
from discord.opus import Decoder
from discord.reader import AudioSink, WaveSink

import speech_recognition as sr
import io
import audioop
import wave
import asyncio
import threading
import asyncio
# from multiprocessing import Process, Queue
import collections
import sys
# sys.path.append("snowboy_location")
# import snowboydetect
# sys.path.pop()
import warnings
from queue import Queue

# warnings.filterwarnings("ignore")

bot = commands.Bot(command_prefix='bruh ')
bot.remove_command('help')

if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus.so')

async def loop():
    while True:
        print("bruh")
        await asyncio.sleep(2)


task = None
@bot.command()
async def test(ctx):
    # vc = await ctx.author.voice.channel.connect()
    # vc.listen(sink)
    # await asyncio.sleep(3)
    # future = asyncio.ensure_future(sink.processAudio())

    task = asyncio.create_task(loop())

@bot.command()
async def print(ctx):
    print("got it")
    await ctx.send("hmmmm")

@bot.command()
async def cancel(ctx):
    print("cancelling")
    task.cancel()

# if __name__ == "__main__":

with open('../src/token.txt', 'r') as f:
    TOKEN = f.readline()

bot.run(TOKEN)