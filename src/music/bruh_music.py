import random
import discord
from discord.ext import commands
import datetime
from mediawikiapi import MediaWikiAPI
from bs4 import BeautifulSoup
from .checks import voice_connected
from ..util import verbosify

JOJOS = ['https://www.youtube.com/watch?v=tHAGig0Mq6o', 'https://www.youtube.com/watch?v=P-3GOo_nWoc&t=38s',
         'https://www.youtube.com/watch?v=ITMjAeWz5hk', 'https://www.youtube.com/watch?v=cPCLFtxpadE',
         'https://www.youtube.com/watch?v=NFjE5A4UAJI', 'https://www.youtube.com/watch?v=So54Khf7bB8',
         'https://www.youtube.com/watch?v=J69VjA6wUQc', 'https://youtu.be/7bF5nk7oRQk',
         'https://www.youtube.com/watch?v=9yGGNohmAT0', 'https://www.youtube.com/watch?v=lWe1nmWeMug&t=3s',
         'https://www.youtube.com/watch?v=fM6mydIVAGY', 'https://youtu.be/JyvjeDtdq3k',
         ]

GIOGIOS = ['https://www.youtube.com/watch?v=tLyRpGKWXRs', 'https://www.youtube.com/watch?v=tLyRpGKWXRs',
           'https://www.youtube.com/watch?v=tLyRpGKWXRs', 'https://www.youtube.com/watch?v=tLyRpGKWXRs',
           'https://www.youtube.com/watch?v=2MtOpB5LlUA',
           ]

SMASH = ['https://www.youtube.com/watch?v=EhgDibw7vB4', 'https://www.youtube.com/watch?v=-70Tmxcf_2g',
         'https://www.youtube.com/watch?v=PInuVXgxO1g', 'https://www.youtube.com/watch?v=PInuVXgxO1g',
         'https://www.youtube.com/watch?v=eWSU8YOa3jU', 'https://www.youtube.com/watch?v=Damxx4K_Yo8',
         'https://www.youtube.com/watch?v=q6R_cZHZZTo', 'https://www.youtube.com/watch?v=bDQUu9Q4-6Y',
         'https://www.youtube.com/watch?v=bDQUu9Q4-6Y', 'https://www.youtube.com/watch?v=bDQUu9Q4-6Y',
         'https://youtu.be/JfB0beI3OOU',
         ]

PENDIS = ['https://www.youtube.com/watch?v=X_hDLdwe7E8', 'https://www.youtube.com/watch?v=SNEBePtkG6U',
          'https://www.youtube.com/watch?v=my6icTjqsW8', 'https://www.youtube.com/watch?v=mNGRkOgZo1M',
          'https://www.youtube.com/watch?v=P_Lwtl85ADs'
          ]

HELLOS = ['https://www.youtube.com/watch?v=7ZtyJK6mgLQ', 'https://www.youtube.com/watch?v=nlLhw1mtCFA',
          'https://www.youtube.com/watch?v=3Njvr6-OVao', 'https://www.youtube.com/watch?v=z6-FWJteNLI'
          ]


class BruhMusic(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.play_cmd = self.bot.get_command("play youtube")

    @commands.command(name='onjah', aliases=['on', 'jah', 'on_jah', 'on-jah', 'X'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def onjah_(self, ctx):
        await ctx.invoke(self.play_cmd, query='https://www.youtube.com/watch?v=EiUjYQgsmwA')
        await ctx.send('https://c7.uihere.com/files/510/792/52/jocelyn-flores-music-sad-club-dread-thumb.jpg')

    @commands.command(name='moment')
    async def bruh_moment_(self, ctx):
        await ctx.invoke(self.play_cmd, query='https://www.youtube.com/watch?v=2ZIpFytCSVc')

    @commands.command(name='go')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sicko_mode_(self, ctx, *args):
        check = ''
        for word in args:
            check += word
        if check == 'sickomode':
            await ctx.invoke(self.play_cmd, query='https://www.youtube.com/watch?v=qMc6xlZaxYA')
            await ctx.send('https://media1.giphy.com/media/1oE3Ee4299mmXN8OYb/source.gif')

    @commands.command(name='jojo')
    async def jojo_(self, ctx, idx: int = None):
        if idx is None:
            await ctx.invoke(self.play_cmd, query=random.choice(JOJOS))
        else:
            await ctx.invoke(self.play_cmd, query=JOJOS[idx])

    @commands.command(name='giogio', aliases=['muda', 'piano', 'gangstar'])
    async def giogio_(self, ctx):
        await ctx.invoke(self.play_cmd, query=random.choice(GIOGIOS))

    @commands.command(name='pendi', aliases=['ruok', '24/7lofihiphop', 'chilledcow'])
    async def pendi_(self, ctx):
        await ctx.invoke(self.play_cmd, query=random.choice(PENDIS))

    @commands.command(name='oof', aliases=['roblox', 'bigoof'])
    async def oof_(self, ctx):
        await ctx.invoke(self.play_cmd, query='https://www.youtube.com/watch?v=hLjTqH_ZvO4')

    @commands.command(name='xgames', aliases=['omahgahd', 'heonxgames'])
    async def xgames_(self, ctx):
        await ctx.invoke(self.play_cmd, query='https://www.youtube.com/watch?v=OWl_HlyHeVc')

    @commands.command(name='obama', aliases=['mrflag', 'president'])
    async def obama_(self, ctx):
        await ctx.invoke(self.play_cmd, query='https://www.youtube.com/watch?v=TuTZjZ6lPxo')

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
        #     await ctx.invoke(self.play_cmd, query=song)

    @commands.command(name='that')
    async def that_(self, ctx, *args):
        mediawikiapi = MediaWikiAPI()

        # get random articles and number
        rand_articles, rand_num = mediawikiapi.random(
            2), random.randint(0, 16777215)
        article_md = ['[{}]({})'.format(article, 'https://en.wikipedia.org/wiki/' +
                                        article.replace(' ', '_')) for article in rand_articles]

        # create embed
        if not args or args[0] not in ['verbose', 'verbosify']:  # zero or wrong arguments
            embed = discord.Embed(color=discord.Color(
                rand_num), description='That is so {1}, can we hit {0} {2}'.format(rand_num, *article_md))
        else:  # either verbose or verbosify
            embed = discord.Embed(color=discord.Color(
                rand_num), description='**That is so {1}, can we hit {0} {2}**'.format(rand_num, *article_md))
            article_descriptions = [mediawikiapi.summary(
                article, chars=150, auto_suggest=False) for article in rand_articles]

            if args[0] == 'verbose':
                [embed.add_field(name="** **", value=desc, inline=True)
                 for desc in article_descriptions]
            elif args[0] == 'verbosify':
                [embed.add_field(name="** **", value=verbosify.verbosify(desc),
                                 inline=True) for desc in article_descriptions]

        await ctx.send(embed=embed)

    @commands.command(name='finna', aliases=['smash', 'finna_smash', 'finna-smash'])
    async def finna_(self, ctx, *args):
        await ctx.invoke(self.play_cmd, query=random.choice(SMASH))

    @commands.command(name='shid')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @voice_connected()
    async def shid_(self, ctx, time: int = 10):
        end = datetime.datetime.now() + datetime.timedelta(seconds=time)
        while datetime.datetime.now() < end:
            try:
                await ctx.invoke(self.bot.get_command("connect"))
                await ctx.voice_client.disconnect()
            except:
                await ctx.voice_client.disconnect()
                pass

    @commands.command(name='hello', aliases=['howdy', 'hola', 'harro eburynyan'])
    async def hello_(self, ctx):
        await ctx.invoke(self.play_cmd, query=random.choice(HELLOS))

