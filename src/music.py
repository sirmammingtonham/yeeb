import asyncio
import discord
import random
import requests
import json
from discord.ext import commands
from mediawikiapi import MediaWikiAPI
from bs4 import BeautifulSoup

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            # await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('You are not in a voice channel.')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, before_options=beforeArgs, after=state.toggle_next)
        except Exception as e:
            fmt = 'oof, you done fucked up: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Queued ' + str(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def warudo(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await self.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await self.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def whatsthisfire(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))

    async def playurl(self, ctx, *, song : str, vol=0.6):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, before_options=beforeArgs, after=lambda: asyncio.run_coroutine_threadsafe(ctx.inxove(self.stop)))
        except Exception as e:
            fmt = 'oof, you done fucked up: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = vol
            entry = VoiceEntry(ctx.message, player)
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def onjah(self, ctx):
        await ctx.invoke(self.stop)
        await self.playurl(ctx, song='https://www.youtube.com/watch?v=fGZb5SpRCi0', vol=10)
        await self.bot.say('https://c7.uihere.com/files/510/792/52/jocelyn-flores-music-sad-club-dread-thumb.jpg')

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def moment(self, ctx):
        await ctx.invoke(self.stop)
        await self.playurl(ctx, song='https://www.youtube.com/watch?v=2ZIpFytCSVc')

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def go(self, ctx, *args):
        check = ''
        for word in args:
            check += word
        if check == 'sickomode':
            await ctx.invoke(self.stop)
            await self.playurl(ctx, song='https://www.youtube.com/watch?v=qMc6xlZaxYA', vol=10)
            await self.bot.say('https://media1.giphy.com/media/1oE3Ee4299mmXN8OYb/source.gif')

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def jojo(self, ctx):
        jojos = ['https://www.youtube.com/watch?v=tHAGig0Mq6o', 'https://www.youtube.com/watch?v=P-3GOo_nWoc&t=38s', 
         'https://www.youtube.com/watch?v=ITMjAeWz5hk', 'https://www.youtube.com/watch?v=cPCLFtxpadE',
         'https://www.youtube.com/watch?v=NFjE5A4UAJI', 'https://www.youtube.com/watch?v=So54Khf7bB8',
         'https://www.youtube.com/watch?v=J69VjA6wUQc',
        ]
        await ctx.invoke(self.stop)
        await self.playurl(ctx, song=random.choice(jojos))

    @commands.command(pass_context=True, no_pm=True)
    async def this(self, ctx, *args):
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            mediawikiapi = MediaWikiAPI()
            await self.bot.say(f'This is so {mediawikiapi.random()}, can we hit {random.randint(0,10000000)} {mediawikiapi.random()}')
        else:
            r=requests.get('https://www.billboard.com/charts/hot-100')
            soup = BeautifulSoup(r.text, 'html.parser')
            div = soup.find('div', {'class': 'chart-list chart-details__left-rail'})
            songs_list = json.loads(div.attrs['data-video-playlist'])
            songs = [x["title"] for x in songs_list]
            song = random.choice(songs)
            song_split = song.split(' - ')

            await self.bot.say(f'This is so sad, Alexa play {song_split[0]} by {song_split[-1]}')
            await ctx.invoke(self.stop)
            await self.playurl(ctx, song=song)

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def finna(self, ctx, *args):
        check = ''
        for word in args:
            check += word
        if check == 'smash':
            smash = ['https://www.youtube.com/watch?v=EhgDibw7vB4', 'https://www.youtube.com/watch?v=-70Tmxcf_2g', 
             'https://www.youtube.com/watch?v=PInuVXgxO1g', 'https://www.youtube.com/watch?v=PInuVXgxO1g',
             'https://www.youtube.com/watch?v=eWSU8YOa3jU', 'https://www.youtube.com/watch?v=Damxx4K_Yo8',
             'https://www.youtube.com/watch?v=q6R_cZHZZTo', 'https://www.youtube.com/watch?v=bDQUu9Q4-6Y',
             'https://www.youtube.com/watch?v=bDQUu9Q4-6Y', 'https://www.youtube.com/watch?v=bDQUu9Q4-6Y',
             'https://www.youtube.com/watch?v=JfB0beI3OOU&list=LL0irG5cbAEYFDzryfNp3Htg&index=7&t=0s',
            ]
            await ctx.invoke(self.stop)
            await self.playurl(ctx, song=random.choice(smash))

def setup(bot):
    bot.add_cog(Music(bot))