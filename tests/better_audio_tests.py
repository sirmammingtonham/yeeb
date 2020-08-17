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

warnings.filterwarnings("ignore")

bot = commands.Bot(command_prefix='bruh ')
bot.remove_command('help')

if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus.so')


async def on_ready():
    # await bot.change_presence(activity=discord.Game(name="testing shid"))
    print('we back')

bot.add_listener(on_ready)

class DiscordPCMStream(sr.AudioSource):
    """
    pls work
    """

    def __init__(self, data):
        self.stream = None

        self.stream_data = data
        self.little_endian = True  # RIFF WAV is a little-endian format (most ``audioop`` operations assume that the frames are stored in little-endian form)
        self.SAMPLE_RATE = Decoder.SAMPLING_RATE
        self.CHUNK = Decoder.FRAME_SIZE  # 3840
        self.SAMPLE_WIDTH = Decoder.SAMPLE_SIZE//Decoder.CHANNELS
        self.FRAME_COUNT = None
        self.DURATION = None

        self.q = Queue()

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"

        self.stream = DiscordPCMStream.PCMStream(self.stream_data, self.SAMPLE_WIDTH)

        self.FRAME_COUNT = self.stream_data.qsize()*self.CHUNK  #len(b"".join(self.stream_data))
        self.DURATION = self.FRAME_COUNT / float(self.SAMPLE_RATE)

        print(f"FRAME COUNT: {self.FRAME_COUNT}")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream = None
        self.DURATION = None
    
    # def updateStream(self):
    #     self.stream = DiscordPCMStream.PCMStream(self.stream_data, self.SAMPLE_WIDTH)

    class PCMStream(object):
        def __init__(self, stream_data, sample_width):
            self.stream_data = stream_data  # an audio file object (e.g., a `wave.Wave_read` instance)
            self.SAMPLE_WIDTH = sample_width
            self.bytesPosition = 0

        def read(self, sample_offset=0):
            buffer = self.stream_data.get()
            buffer = audioop.tomono(buffer, self.SAMPLE_WIDTH, 1, 1)  # convert stereo audio data to mono (this is the part that fucked me up bruh)
            return buffer

class TestSink(AudioSink):
    def __init__(self):
        self.data = Queue()
        self.needs_processing = True
        self.r = sr.Recognizer()
        self.stream = DiscordPCMStream(self.data)
        self.processing = False
        self.stop = False


    async def processAudio(self):
        while not self.stop:
            with self.stream as s:
                audio = self.r.listen(s, snowboy_configuration=(
                    "../src/audio/snowboy", ["../src/audio/snowboy/bruh.pmdl"]
                ))
                print(self.r.recognize_google(audio))
                with open("pls.wav", "wb+") as f:
                    f.write(audio.get_wav_data())


    def write(self, data):
        self.data.put(data.data)

    def read(self):
        pass

    def cleanup(self):
        pass


sink = TestSink()

def callback(audio):
    print("callback called")
    with open("pls.wav", "wb+") as f:
        f.write(audio.get_wav_data())
    # print(audio.get_raw_data())

@bot.command()
async def test(ctx):
    vc = await ctx.author.voice.channel.connect()
    vc.listen(sink)
    await asyncio.sleep(3)
    # future = asyncio.ensure_future(sink.processAudio())

    asyncio.create_task(sink.processAudio())

@bot.command()
async def print(ctx):
    print("got it")
    await ctx.send("hmmmm")

@bot.command()
async def process(ctx):
    sink.processAudio()

@bot.command()
async def cancel(ctx):
    print("cancelling")
    sink.stop = True
    future.cancel()

# if __name__ == "__main__":

with open('../src/token.txt', 'r') as f:
    TOKEN = f.readline()

bot.run(TOKEN)