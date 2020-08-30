import asyncio
import discord
from discord.ext import commands

from audio import DiscordPCMStream, TranscriptionSink, AudioClasses

if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus.so')

class Speech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.sink = None
        self.vc = None
        self.command_mapping = None
        self.task = None

    async def recognizer_callback(self, audio_data):
        try:
            pred = await self.sink.recognize_google_cloud(audio_data, 
                list(self.command_mapping.keys()),
                credentials_json="audio/yeeb-cloud.json",
                show_all=False
            )

            pred = pred.lower() # make all heard words lower

            print(f'detected {pred}')
            if pred.strip()[0] in self.bot.commands:
                try:
                    pred = pred.strip()
                    await self.ctx.invoke(self.bot.get_command(pred[0]), query=' '.join(pred[1]))
                except Exception as e:
                    print(f"error invoking {pred}: {e}")
                    await self.ctx.send("bruh momenti", delete_after=15)
            else:
                await self.ctx.send("no understando", delete_after=15)

        except AudioClasses.UnknownValueError as e:
            await self.ctx.send("no understando", delete_after=15)
            print(e)

    @commands.command(name='listen', aliases=['alexa', 'hear me out'])
    async def listen(self, ctx):
        if self.sink is None:
            self.sink = TranscriptionSink(self.recognizer_callback, asyncio.get_event_loop())

        self.ctx = ctx
        self.vc = ctx.voice_client
        if self.vc is None:
            try:
                self.vc = await ctx.author.voice.channel.connect()
            except asyncio.TimeoutError:
                print(f"shid happen: {e}")

        if not self.vc.is_listening():
            self.vc.listen(self.sink)
            await asyncio.sleep(1)  # record some data before trying to listen
            self.task = asyncio.create_task(self.sink.initListenerLoop())
            await ctx.send("👁👄👁")
        else:
            await ctx.send("already listening bruh")

    @commands.command(name='cancel', aliases=['unlisten'])
    async def cancel(self, ctx):
        if self.task is not None and not self.task.cancelled():
            self.sink.cleanup()
            self.task.cancel()
        self.vc.stop_listening()
        print("stopped listening")

def setup(bot):
    speech = Speech(bot)
    bot.add_cog(speech)

    command_mapping = {
        # true if has args, false otherwise
        # bruh.py
        "help": (bot.get_command('help'), False),
        "clear": (bot.get_command('clear'), False),
        # "snap": (bot.get_command('snap'), False),
        "spam": (bot.get_command('spam'), True),
        "cringe": (bot.get_command('thatsprettycringe'), False),
        "how long": (bot.get_command('howlong'), False),
        "code": (bot.get_command('code'), False),
        "censor": (bot.get_command('censor'), True),
        "invite": (bot.get_command('invite'), False),
        "die": (bot.get_command('die'), False),
        "swear": (bot.get_command('swear'), False),
        "swearat": (bot.get_command('swearat'), True),

        "jacobify": (bot.get_command('jacobify'), True),
        "prolixify": (bot.get_command('prolixify'), True),
        "verbosify": (bot.get_command('verbosify'), True),

        "cumber": (bot.get_command('cumber'), False),
        "girl cumber": (bot.get_command('girlcumber'), False),
        "cum": (bot.get_command('cum'), False),
        "korra": (bot.get_command('korra'), False),
        "valortne": (bot.get_command('valortne'), False),

        # card.py?
        "shitty hearthstone": (bot.get_command('shitty hearthstone'), False),
        "hearthstone join": (bot.get_command('hearthstone join'), False),
        "hearthstone reset": (bot.get_command('hearthstone reset'), False),
        "time to duel": (bot.get_command('hearthstone itstimetoduel'), False),

        # music.py
        "connect": (bot.get_command('connect'), True),
        "play": (bot.get_command('play'), True),
        "now playing": (bot.get_command('now playing'), False),
        "on jah": (bot.get_command('onjah'), False),
        "moment": (bot.get_command('moment'), False),
        "sicko mode": (bot.get_command('go'), False),
        "jo jo": (bot.get_command('jojo'), False),
        "gio gio": (bot.get_command('giogio'), False),
        "pendi": (bot.get_command('pendi'), False),
        "oof": (bot.get_command('oof'), False),
        "x games": (bot.get_command('xgames'), False),
        "this": (bot.get_command('this'), False),
        "that": (bot.get_command('that'), False),
        "finna": (bot.get_command('finna'), False),
        "stop": (bot.get_command('stop'), False),
        "shid": (bot.get_command('shid'), False),

        # speech.py
        # "listen": (bot.get_command('listen'), False),
        "cancel": (bot.get_command('cancel'), False),
    }
    speech.command_mapping = command_mapping

    print('Speech module loaded.')