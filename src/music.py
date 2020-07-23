"""
https://github.com/MASERBOSS/dj-wala-babu
"""
import os
import discord
from discord.ext import commands

import asyncio
import itertools, datetime
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from discord.ext.commands.cooldowns import BucketType

import random
import requests
import json
from mediawikiapi import MediaWikiAPI
from bs4 import BeautifulSoup

ytdlopts = {
    'username': os.environ['YOUTUBE_USER'],
    'password': os.environ['YOUTUBE_PASS'],
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin -preset ultrafast',
    'options': '-vn -threads 1'
}

jojos = ['https://www.youtube.com/watch?v=tHAGig0Mq6o', 'https://www.youtube.com/watch?v=P-3GOo_nWoc&t=38s', 
    'https://www.youtube.com/watch?v=ITMjAeWz5hk', 'https://www.youtube.com/watch?v=cPCLFtxpadE',
    'https://www.youtube.com/watch?v=NFjE5A4UAJI', 'https://www.youtube.com/watch?v=So54Khf7bB8',
    'https://www.youtube.com/watch?v=J69VjA6wUQc', 'https://youtu.be/7bF5nk7oRQk',  
    'https://www.youtube.com/watch?v=9yGGNohmAT0', 'https://www.youtube.com/watch?v=lWe1nmWeMug&t=3s',
    'https://www.youtube.com/watch?v=fM6mydIVAGY', 'https://youtu.be/JyvjeDtdq3k',
]

giogios = ['https://www.youtube.com/watch?v=tLyRpGKWXRs', 'https://www.youtube.com/watch?v=tLyRpGKWXRs', 
    'https://www.youtube.com/watch?v=tLyRpGKWXRs', 'https://www.youtube.com/watch?v=tLyRpGKWXRs',
    'https://www.youtube.com/watch?v=2MtOpB5LlUA',
]

smash = ['https://www.youtube.com/watch?v=EhgDibw7vB4', 'https://www.youtube.com/watch?v=-70Tmxcf_2g', 
    'https://www.youtube.com/watch?v=PInuVXgxO1g', 'https://www.youtube.com/watch?v=PInuVXgxO1g',
    'https://www.youtube.com/watch?v=eWSU8YOa3jU', 'https://www.youtube.com/watch?v=Damxx4K_Yo8',
    'https://www.youtube.com/watch?v=q6R_cZHZZTo', 'https://www.youtube.com/watch?v=bDQUu9Q4-6Y',
    'https://www.youtube.com/watch?v=bDQUu9Q4-6Y', 'https://www.youtube.com/watch?v=bDQUu9Q4-6Y',
    'https://youtu.be/JfB0beI3OOU',
]

pendis = ['https://www.youtube.com/watch?v=X_hDLdwe7E8', 'https://www.youtube.com/watch?v=SNEBePtkG6U', 
    'https://www.youtube.com/watch?v=my6icTjqsW8', 'https://www.youtube.com/watch?v=mNGRkOgZo1M'
]

ytdl = YoutubeDL(ytdlopts)

if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus.so')


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')

        if self.title is None:
            self.title = "No title available"

        self.web_url = data.get('webpage_url')
        self.thumbnail = data.get('thumbnail')

        if self.thumbnail is None:
            self.thumbnail = "https://www.pikpng.com/pngl/m/133-1330743_peter-griffin-png-family-guy-t-pose-transparent.png"

        self.duration = data.get('duration')

        if self.duration is None:
            self.duration = 0

        self.uploader = data.get('uploader')

        if self.uploader is None:
            self.uploader = "Unknown uploader"
        
        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f':notes: Added to queue: **{data["title"]}**')

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_ctxs', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'buttons', 'music', 'music_controller', 'restmode')

    def __init__(self, ctx):

        self.buttons = {'⏯': 'rp',
                        '⏭': 'skip',
                        '➕': 'vol_up',
                        '➖': 'vol_down',
                        '🖼': 'thumbnail',
                        '⏹': 'stop',
                        'ℹ': 'queue',
                        '❔': 'tutorial'}

        self.bot = ctx.bot
        self._guild = ctx.guild
        self._ctxs = ctx
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None
        self.music_controller = None

        ctx.bot.loop.create_task(self.player_loop())

    async def buttons_controller(self, guild, current, source, channel, context):
        vc = guild.voice_client
        vctwo = context.voice_client

        for react in self.buttons:
            await current.add_reaction(str(react))

        def check(r, u):
            if not current:
                return False
            elif str(r) not in self.buttons.keys():
                return False
            elif u.id == self.bot.user.id or r.message.id != current.id:
                return False
            elif u not in vc.channel.members:
                return False
            elif u.bot:
                return False
            return True

        while current:
            if vc is None:
                return False

            react, user = await self.bot.wait_for('reaction_add', check=check)
            control = self.buttons.get(str(react))

            if control == 'rp':
                if vc.is_paused():
                    vc.resume()
                else:
                    vc.pause()

            if control == 'skip':
                vc.stop()

            if control == 'stop':
                await channel.send('**:notes: aight imma head out.**', delete_after=5)
                await self._cog.cleanup(guild)

                try:
                    self.music_controller.cancel()
                except:
                    pass

            if control == 'vol_up':
                player = self._cog.get_player(context)
                vctwo.source.volume += 5
                        
            if control == 'vol_down':
                player = self._cog.get_player(context)
                vctwo.source.volume -= 5

            if control == 'thumbnail':
                await channel.send(embed=discord.Embed(color=self.bot.user.color).set_image(url=source.thumbnail).set_footer(text=f"Requested by {source.requester} | Video: {source.title}", icon_url=source.requester.avatar_url), delete_after=10)

            if control == 'tutorial':
                await channel.send(embed=discord.Embed(color=self.bot.user.color).add_field(name="How to use Music Controller?", value="⏯ - Resume or pause player\n⏭ - Skip song\n➕ - Volume up\n➖ - Volume down\n🖼 - Get song info\n⏹ - Stop music session\nℹ - Player queue\n❔ - Shows you how to use Music Controller"), delete_after=10)
            
            if control == 'queue':
                await self._cog.queue_info(context)

            try:
                await current.remove_reaction(react, user)
            except discord.HTTPException:
                pass

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(3500):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f':notes: oof your link is bad. or maybe you\'re bad. or maybe we\'re bad.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source
            try:
                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            except Exception:
                continue
            embednps = discord.Embed(color=self.bot.user.color)
            embednps.add_field(name="Song title:", value=f"```fix\n{source.title}```", inline=False)
            embednps.add_field(name="Requested by:", value=f"**{source.requester}**", inline=True)
            embednps.add_field(name="Song URL:", value=f"**[CLICK IF YOU DARE]({source.web_url})**", inline=True)
            embednps.add_field(name="Uploader:", value=f"**{source.uploader}**", inline=True)
            embednps.add_field(name="Song duration:", value=f"**{datetime.timedelta(seconds=source.duration)}**", inline=True)
            embednps.set_thumbnail(url=f"{source.thumbnail}")
            self.np = await self._channel.send(embed=embednps)

            self.music_controller = self.bot.loop.create_task(self.buttons_controller(self._guild, self.np, source, self._channel, self._ctxs))
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
                self.music_controller.cancel()
            except Exception:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))

class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players', 'musictwo', 'music_controller')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(':notes: This command can not be used in the dms.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send(":notes: Not in a voice channel nerd. Certified bruh moment right here...")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='connect', aliases=['join', 'j'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send(":notes: Not in a voice channel nerd. Join one or specify one with this command.")

        vc = ctx.voice_client
        
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out. :regional_indicator_f: ')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out. :regional_indicator_f: ')

        await ctx.send(f":notes: Connected to channel: **{channel}**", delete_after=20)
        
    @commands.command(name='play', aliases=['p', 'pp'])
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        elif ctx.author not in ctx.guild.voice_client.channel.members:
            return await ctx.send(":notes: You're the reason why we can't have nice things. Join my voice channel to execute this command. smh my head.", delete_after=20)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
        await player.queue.put(source)


    @commands.command(name='whatsthisfire', aliases=['np', 'current', 'currentsong', 'playing', 'what\'sthisfire'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(":notes: You're the reason why we can't have nice things. I am not connected to voice or playing anything. smh your head.", delete_after=20)

        elif ctx.author not in ctx.guild.voice_client.channel.members:
            return await ctx.send(":notes: We aren't even in the same channel. these gamers aint loyal.", delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send(":notes: You're the reason why we can't have nice things. I am not connected to voice or playing anything. smh the person who added me to this server's head.", delete_after=20)

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except discord.HTTPException:
            pass

        embednp = discord.Embed(color=self.bot.user.color)
        embednp.add_field(name="Song title:", value=f"```fix\n{vc.source.title}```", inline=False)
        embednp.add_field(name="Requested by:", value=f"**{vc.source.requester}**", inline=True)
        embednp.add_field(name="Song URL:", value=f"**[URL]({vc.source.web_url})**", inline=True)
        embednp.add_field(name="Uploader:", value=f"**{vc.source.uploader}**", inline=True)
        embednp.add_field(name="Song duration:", value=f"**{datetime.timedelta(seconds=vc.source.duration)}**", inline=True)
        embednp.set_thumbnail(url=f"{vc.source.thumbnail}")
        player.np = await ctx.send(embed=embednp)
        self.music_controller = self.bot.loop.create_task(MusicPlayer(ctx).buttons_controller(ctx.guild, player.np, vc.source, ctx.channel, ctx))

    async def queue_info(self, ctx):
        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('**:notes: There are currently no more queued songs.**')

        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Queue - Next {len(upcoming)}', description=fmt, color=self.bot.user.color)
        await ctx.send(embed=embed)

    @commands.command(name='onjah', aliases=['on jah', 'on_jah', 'on-jah', 'x'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def onjah_(self, ctx):
        await self.play_.callback(self, ctx, search='https://www.youtube.com/watch?v=fGZb5SpRCi0')
        await ctx.send('https://c7.uihere.com/files/510/792/52/jocelyn-flores-music-sad-club-dread-thumb.jpg')

    @commands.command(name='moment')
    async def bruh_moment_(self, ctx):
        await self.play_.callback(self, ctx, search='https://www.youtube.com/watch?v=2ZIpFytCSVc')

    @commands.command(name='go')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sicko_mode_(self, ctx, *args):
        check = ''
        for word in args:
            check += word
        if check == 'sickomode':
            await self.play_.callback(self, ctx, search='https://www.youtube.com/watch?v=qMc6xlZaxYA')
            await ctx.send('https://media1.giphy.com/media/1oE3Ee4299mmXN8OYb/source.gif')

    @commands.command(name='jojo')
    async def jojo_(self, ctx, idx:int=None):
        if idx is None:
            await self.play_.callback(self, ctx, search=random.choice(jojos))
        else:
            await self.play_.callback(self, ctx, search=jojos[idx])

    @commands.command(name='giogio', aliases=['muda', 'piano', 'gangstar'])
    async def giogio_(self, ctx):
        await self.play_.callback(self, ctx, search=random.choice(giogios))
                        
    @commands.command(name='pendi', aliases=['r u ok', '24/7 lofi hip hop', 'chilledcow'])
    async def pendi_(self, ctx):
        await self.play_.callback(self, ctx, search=random.choice(pendis))
                        
    @commands.command(name='oof', aliases=['roblox', 'big oof'])
    async def oof_(self, ctx):
        await self.play_.callback(self, ctx, search='https://www.youtube.com/watch?v=hLjTqH_ZvO4')

    @commands.command(name='this')
    async def this_(self, ctx, *args):
        # vc = ctx.voice_client
        # if not vc or not vc.is_connected():
        mediawikiapi = MediaWikiAPI()
        await ctx.send(f'This is so {mediawikiapi.random()}, can we hit {random.randint(0,10000000)} {mediawikiapi.random()}')
        # else:
        #     r=requests.get('https://www.billboard.com/charts/hot-100')
        #     soup = BeautifulSoup(r.text, 'html.parser')
        #     div = soup.find('div', {'class': 'chart-list chart-details__left-rail'})
        #     songs_list = json.loads(div.attrs['data-video-playlist'])
        #     songs = [x["title"] for x in songs_list]
        #     song = random.choice(songs)
        #     song_split = song.split(' - ')

        #     await ctx.send(f'This is so sad, Alexa play {song_split[0]} by {song_split[-1]}')
        #     await self.play_.callback(self, ctx, search=song)

    @commands.command(name='finna', aliases=['smash', 'finna_smash', 'finna-smash'])
    async def finna_(self, ctx, *args):
        await self.play_.callback(self, ctx, search=random.choice(smash))
    
    @commands.command(name='stop', aliases=['disconnect', 'dc', 'gtfo'])
    async def dc_(self, ctx):
        await ctx.send('Try pressing the stop button next time bruhheadass.')
        await ctx.guild.voice_client.disconnect()

    @commands.command(name='shid')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shid_(self, ctx, time:int=10):
        vc = ctx.voice_client
        if not vc:
            await ctx.send('You are not in a voice channel. You must subject yourself to this command to use it.')
            return False

        end = datetime.datetime.now() + datetime.timedelta(seconds=time)
        while datetime.datetime.now() < end:
            try:
                await ctx.invoke(self.connect_)
                await ctx.guild.voice_client.disconnect()
            except:
                await ctx.guild.voice_client.disconnect()
                pass


def setup(bot):
    bot.add_cog(Music(bot))
    print('Music module loaded.')
