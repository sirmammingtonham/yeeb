import discord
from discord.ext import commands

from audio import DiscordPCMStream, TranscriptionSink
import speech_recognition as sr

class Speech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sink = None
        self.r = sr.Recognizer()

        if not discord.opus.is_loaded():
            discord.opus.load_opus('libopus.so')

    @staticmethod
    def recognizerCallback(recognizer_instance, audio_data):
        with open("pain.wav", "wb+") as f:
            f.write(audio_data.get_wav_data())
        # try:
        print(recognizer_instance.recognize_google(audio_data, show_all=True))
        # except Exception as e:
        #     print(e)

    @commands.command(name='listen', aliases=['hear me out'])
    async def listen(self, ctx):
        if self.sink is None:
            sink = TranscriptionSink(self.r, Speech.recognizerCallback)
        try:
            vc = await ctx.author.voice.channel.connect()
        except Exception as e:
            print("shid happen: {e}")
        
        vc.listen(sink)

        sink.processAudio()

def setup(bot):
    bot.add_cog(Speech(bot))
    print('Speech module loaded.')