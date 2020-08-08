import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import random
import requests
from dateutil.relativedelta import relativedelta
from apex_legends import ApexLegends

from nltk.corpus import wordnet
import cv2
import numpy as np
from io import BytesIO

import verbosify
import time

from PyDictionary import PyDictionary
dictionary = PyDictionary()

def user_is_me(ctx):
    return ctx.author.id == 228017779511394304

def user_is_bot_contributor(ctx):
    return ctx.author.id == 228017779511394304 or ctx.author.id == 150093212034269184 or ctx.author.id == 188179573484158976

class Bruh(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def apex(self, ctx, player:str):
        if ctx.invoked_subcommand is None:
            apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
            try:
                player = apex.player(player)
            except:
                await ctx.send('Player not found')
                return
            embed = discord.Embed(
                 colour = discord.Colour.blue()
                 )
            embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
            embed.set_thumbnail(url=player.legends[0].icon)
            embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
            embed.add_field(name='Level:', value=player.level, inline=False)
            # for legend in player.legends:
            #   embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
            for a in dir(player.legends[0]):
                if a == 'damage' or 'kills' in a:
                    name = a + ':'
                    embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
            await ctx.send(embed=embed)

    @apex.command()
    async def xbox(self, ctx, *args):
        apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
        try:
            name = ''
            for word in args:
                name += word + ' '
            player = apex.player(name, plat=1)
        except:
            await ctx.send('Player not found')
            return
        embed = discord.Embed(
             colour = discord.Colour.blue()
             )
        embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
        embed.set_thumbnail(url=player.legends[0].icon)
        embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
        embed.add_field(name='Level:', value=player.level, inline=False)
        # for legend in player.legends:
        #   embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
        for a in dir(player.legends[0]):
            if a == 'damage' or 'kills' in a:
                name = a + ':'
                embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
        await ctx.send(embed=embed)

    @apex.command()
    async def psn(self, ctx, player:str):
        apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
        try:
            player = apex.player(player, plat=2)
        except:
            await ctx.send('Player not found')
            return
        embed = discord.Embed(
             colour = discord.Colour.blue()
             )
        embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
        embed.set_thumbnail(url=player.legends[0].icon)
        embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
        embed.add_field(name='Level:', value=player.level, inline=False)
        # for legend in player.legends:
        #   embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
        for a in dir(player.legends[0]):
            if a == 'damage' or 'kills' in a:
                name = a + ':'
                embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        await ctx.author.send('bet')
        await asyncio.sleep(5)
        await ctx.author.send('https://github.com/sirmammingtonham/yeeb')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=100):
        channel = ctx.message.channel
        def is_pinned(m):
            return not m.pinned
        await channel.purge(limit=amount, check=is_pinned)
        await ctx.send('I\'m still logging all your data lol', delete_after=10)

    @clear.error
    async def clear_error(error, ctx):
        if isinstance(error, MissingPermissions):
            await ctx.send('You don\'t have the power, peasant.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def snap(self, ctx):
        channel = ctx.message.channel
        messages = []
        async for message in ctx.channel.history(after=datetime.now() - timedelta(days=14)):
            if not message.pinned:
                messages.append(message)
        random.shuffle(messages)
        await ctx.channel.delete_messages(messages[:len(messages)//2])
        await ctx.send('perfectly balanced\nhttps://media1.tenor.com/images/d89ba4e965cb9144c82348a1c234d425/tenor.gif?itemid=11793362', delete_after=30)

    @snap.error
    async def snap_error(error, ctx):
        if isinstance(error, MissingPermissions):
            await ctx.send('You don\'t have the power, peasant.')

    @commands.command()
    async def spam(self, ctx, *args):
        if user_is_me(ctx):
            for _ in range(int(args[-1])):
                output = ''
                for word in args[:-1]:
                    output += word + ' '
                await ctx.send(output)
        else:
            await ctx.send('You don\'t have the power, peasant.')

    @commands.command(name='thatsprettycringe', aliases=['that\'sprettycringe', 'naenaebaby', 'cringe'])
    async def thatsprettycringe(self, ctx):
        if random.randint(0,1) == 0:
            await ctx.send('https://scontent-dfw5-1.cdninstagram.com/vp/c282a44720c779936cf34c43152ef8ae/5DED2138/t51.2885-15/e35/66229303_174304563604647_4383371938153947034_n.jpg?_nc_ht=scontent-dfw5-1.cdninstagram.com')
        else:
            await ctx.send('https://pbs.twimg.com/media/EBOgkoXXUAEf7hx.jpg')

    @commands.command(name='howlong', aliases=['schmurda', 'how long'])
    async def howlong(self, ctx):
        td = relativedelta(datetime(2020, 12, 11), datetime.now())
        await ctx.send(f'Bobby Shmurda will be released in {td.years} years, {td.months} months, {td.days} days, {td.hours} hours, {td.minutes} minutes, and {td.seconds} seconds.')

    @commands.command()
    async def code(self, ctx):
        await ctx.send('https://github.com/sirmammingtonham/yeeb')

    @commands.command()
    async def censor(self, ctx, *args, time:int=1):
        channel = ctx.message.channel
        if args is not None:
            user = ''
            for word in args:
                user += word
        elif args.isdigit():
            time = int(args)

        if time > 5:
            await ctx.send('nah')
            return

        end = datetime.now() + timedelta(minutes=time)

        if user in [str(member) for member in ctx.message.guild.members]:
            def check(message):
                return str(message.author) == user and message.channel == channel

            while datetime.now() < end:
                message = await self.bot.wait_for('message', check=check)
                await message.delete()
                await ctx.send(f'||{message.content}||')

        else:
            while datetime.now() < end:
                message = await self.bot.wait_for('message', check=lambda m: m.channel==channel)
                await message.delete()
                await ctx.send(f'||{message.content}||')

    @commands.command()
    async def invite(self, ctx):
        await ctx.send('https://discordapp.com/oauth2/authorize?client_id=547156702626185230&scope=bot&permissions=8')

    @commands.command()
    async def die(self, ctx):
        if user_is_me(ctx):
            await self.bot.logout()
        else:
            await ctx.send('You cannot kill me, peasant.')
            
    @commands.command()
    async def swear(self, ctx):
        words = open("swearwords.txt").readlines()
        word = words[random.randrange(165)][:-1]
        await ctx.send(word)
        
    @commands.command()
    async def swearat(self, ctx, name:str='', num_times:str=''):
        all_words = open("swearwords.txt").readlines()
        selected_words = all_words[random.randrange(165)][:-1]
        
        # see if "twice" or "thrice" is written in the command
        if 'twice' in num_times:
            selected_words += ' ' + all_words[random.randrange(165)][:-1]
        elif 'thrice' in num_times:
            selected_words += ' ' + all_words[random.randrange(165)][:-1] \
                            + ' ' + all_words[random.randrange(165)][:-1]
        elif 'random' in num_times:
            for i in range(random.randint(1, 10)):
                selected_words += ' ' + all_words[random.randrange(165)][:-1]
        
        elif num_times.isdigit():
            for i in range(int(num_times)):
                selected_words += ' ' + all_words[random.randrange(165)][:-1]

        if name == '':
            name = random.choice(ctx.guild.members).mention
        elif not name.startswith('<@'):
            try:
                name = ctx.guild.get_member_named(name).mention
            except:
                name = ctx.author.mention

        # check for long messages
        if len(name + ' is a ' + selected_words) <= 2000:
            await ctx.send(name + ' is a ' + selected_words, delete_after=30)
        else:
            curr_msg = name + ' is a' # build up message up to 2000 characters

            for word in selected_words.split():
                if len(curr_msg + ' ' + word) <= 2000:
                    curr_msg += ' ' + word
                else:  # we've reached the limit
                    await ctx.send(curr_msg, delete_after=30)
                    curr_msg = name + ' is a ' + word  # start it over again

            # send anything left over
            if len('and finally ' + curr_msg) <= 2000: await ctx.send('and finally ' + curr_msg, delete_after=30)
            else:
                second_last_msg, last_word = curr_msg.rsplit(' ', 1)
                await ctx.send(second_last_msg, delete_after=30)
                await ctx.send('and finally ' + name + ' is a ' + last_word, delete_after=30)


            
    @commands.command()    
    async def jacobify(self, ctx, *args):
        message = ''    
        for word in args:
            try:
                message += ' ' + random.choice(dictionary.synonym(word))
            except:
                message += ' ' + word
        await ctx.send(message)

    @commands.command()    
    async def prolixify(self, ctx, *args):
        def _elongate(word):
            if len(word) == 1:
                return word
            longest = word
            for syn in wordnet.synsets(word):
                for lm in syn.lemmas():
                    if len(lm.name()) > len(longest) and lm.name().count('_') == 0:
                        longest = lm.name()
            return longest

        def _randomize(word):
            if len(word) == 1:
                return word
            lemmas = []
            for syn in wordnet.synsets(word):
                lemmas.extend(syn.lemmas())
            if len(lemmas):
                word = random.choice(lemmas).name().replace('_', ' ')
            return word

        message = ''
        if args[0] == "*long":
            for word in args[1:]:
                message += ' ' + _elongate(word)
        elif args[0] == "*random":
            for word in args[1:]:
                message += ' ' + _randomize(word)
        else:
            for word in args:
                if random.random() >= 0.5:
                    message += ' ' + _elongate(word)
                else:
                    message += ' ' + _randomize(word)
        
        await ctx.send(message)
    
    @commands.command()
    async def verbosify(self, ctx, *, input_sentence):
        # get spot to break up message
        def get_breakpoint(msg):
            i = 2000
            while i > 0 and msg[i] != ' ': i -= 1
            
            return 2000 if i is 0 else i
            
        
        num_times = 1
        # Detect num_times argument. gotta check for positive and negative numbers
        if input_sentence.split()[0].isdigit() or input_sentence.split()[0][1:].isdigit():
            num_times = int(input_sentence.split()[0])

            # bruh don't try to break it bruh
            if num_times < 0 or num_times > 500:
                await ctx.send('bruh')
                return

            input_sentence = ' '.join(input_sentence.split()[1:])

        # edge cases
        if num_times is 0:
            await ctx.send(input_sentence)
            return
        elif num_times is 1:
            await ctx.send(verbosify.verbosify(input_sentence))
            return

        # Run verbosify num_times number of times
        to_print = [round(num_times*(i/5)) for i in range(1,5)] # when to print progress
        max_char_count = False

        verbosified = verbosify.verbosify(input_sentence)
        msg = await ctx.send('`[1]` ' + verbosified)
        
        for i in range(2, num_times):
            if len(verbosified) > 10000: break  # would go past 10 messages...
            new_verbosified = verbosify.verbosify(verbosified)
            
            if len(new_verbosified) > 1990 and not max_char_count:
                time.sleep(1)
                await msg.edit(content='`[...]` ' + verbosified)
                max_char_count = True
            else:
                verbosified = new_verbosified

                if i in to_print and len(verbosified) < 1990:
                    time.sleep(1)
                    await msg.edit(content='`[{}]` {}'.format(i, verbosified))

        # Final output
        time.sleep(1)
        verbosified = verbosify.verbosify(verbosified) # one last time
        
        if len(verbosified) <= 2000: await msg.edit(content=verbosified)
        else:
            first_output = True

            # keep looping until message is under 2000
            while len(verbosified) > 2000:
                bp = get_breakpoint(verbosified)

                if first_output:
                    await msg.edit(content=verbosified[:bp])
                    first_output = False
                else: await ctx.send(verbosified[:bp], delete_after=30)
                
                verbosified = verbosified[bp+1:]

            # send last message
            await ctx.send(verbosified, delete_after=30)

        


         
    @commands.command(name='cumber', aliases=['girl cumber'])
    async def cumber(self, ctx):

        def _cumberify(f):
            img = cv2.imdecode(np.fromstring(f.read(), np.uint8), 1)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # convert to hsv colorspace because we get better accuracy?
            lower_green = np.array([25,50,50])
            upper_green = np.array([80,255,255]) # took too damn long to find these values
            mask = cv2.inRange(hsv, lower_green, upper_green) # create mask for all greens and yellows
            mask = mask/255
            mask = mask.astype(np.bool)
            cumbered = np.argwhere(mask) # get idxs of green pixels

            # draw a rectangle around part of the cucumber (20% looks too small in most cases)
            cv2.rectangle(
                img, 
                (cumbered[0][1], cumbered[0][0]), 
                (cumbered[round(len(cumbered)*0.5)][1], cumbered[round(len(cumbered)*0.5)][0]), 
                (0,0,0), 
                -1
            )

            _, buffer = cv2.imencode(".jpg", img)
            return buffer
        
        r = requests.get("https://source.unsplash.com/featured/?cucumber")
        if r.status_code == 200:
            f = BytesIO(r.content)
            # try:
            modified_cumber = _cumberify(f)
            await ctx.send(file=discord.File(BytesIO(modified_cumber), 'cumber.jpg'))
            # except:
            #     await ctx.send("bruh moment occured, try again?")

        else:
            await ctx.send("bruh moment occured, try again?")
    
    @commands.command(name='girlcumber', aliases=['cumber legacy'])
    async def girlcumber(self, ctx):
        r = requests.get("https://source.unsplash.com/featured/?cucumber")
        await ctx.send(r.url)
    
    @commands.command(name='cum', aliases=['nut'])
    async def cum(self, ctx):
        await ctx.send("https://i.pinimg.com/736x/38/e9/57/38e957bb23e73d3759dda419cece5bc0.jpg")

    @commands.command()
    async def korra(self, ctx):
        links = [
            'https://media.discordapp.net/attachments/661185720211341312/739759077302861875/image0.jpg',
            'https://cdn.discordapp.com/attachments/661185720211341312/739748973597818880/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/738668566793945098/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/737209307900149811/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/737203525330665502/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/737203457781530744/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/737203345894408232/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/736516684663226398/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/736511129538265128/unknown.png',
            'https://cdn.discordapp.com/attachments/661185720211341312/733258810713571378/Screenshot_20200716-0248022.png',
        ]

        i = random.randrange(len(links))
        if i == 0: await ctx.send(links[0])
        else: await ctx.send(links[i], delete_after=30)
    
    @commands.command()
    async def valortne(self, ctx, *args):
        agents = {
            'SAGE': 'The bastion of China, Sage creates safety for herself and her team wherever she goes. Able to revive fallen friends and stave off forceful assaults, she provides a calm center to a hellish battlefield.',
            'SOVA': 'Born from the eternal winter of Russia’s tundra, Sova tracks, finds, and eliminates enemies with ruthless efficiency and precision. His custom bow and incredible scouting abilities ensure that even if you run, you cannot hide.',
            'BREACH': 'The bionic Swede Breach fires powerful, targeted kinetic blasts to aggressively clear a path through enemy ground. The damage and disruption he inflicts ensures no fight is ever fair.',
            'VIPER': 'The American Chemist, Viper deploys an array of poisonous chemical devices to control the battlefield and cripple the enemy’s vision. If the toxins don’t kill her prey, her mind games surely will.',
            'BRIMSTONE': 'Joining from the USA, Brimstone’s orbital arsenal ensures his squad always has the advantage. His ability to deliver utility precisely and safely make him the unmatched boots-on-the-ground commander.',
            'CYPHER': 'The Moroccan information broker, Cypher is a one-man surveillance network who keeps tabs on the enemy’s every move. No secret is safe. No maneuver goes unseen. Cypher is always watching.',
            'JETT': 'Representing her home country of South Korea, Jett’s agile and evasive fighting style lets her take risks no one else can. She runs circles around every skirmish, cutting enemies up before they even know what hit them.',
            'OMEN': 'A phantom of a memory, Omen hunts in the shadows. He renders enemies blind, teleports across the field, then lets paranoia take hold as his foe scrambles to uncover where he might strike next.',
            'PHOENIX': 'Hailing from the UK, Phoenix\'s star power shines through in his fighting style, igniting the battlefield with flash and flare. Whether he\'s got backup or not, he\'s rushing in to fight on his own terms.',
            'RAZE': 'Raze explodes out of Brazil with her big personality and big guns. With her blunt-force-trauma playstyle, she excels at flushing entrenched enemies and clearing tight spaces with a generous dose of "boom".',
            'REYNA': 'Forged in the heart of Mexico, Reyna dominates single combat, popping off with each kill she scores. Her capability is only limited by her raw skill, making her sharply dependent on performance.',
            'KILLJOY': 'The genius of Germany, Killjoy secures and defends key battlefield positions with a collection of traps, turrets, and mines. Each invention is primed to punish any assailant too dumb to back down.'
        }
        
        if not args or args[0].upper() not in agents: agent = random.choice(list(agents.values()))
        else: agent = agents[args[0].upper()]
        await ctx.send(verbosify.verbosify(agent))
        
    @commands.command()
    async def shityourpants(self, ctx):
        if user_is_bot_contributor(ctx):
            await self.bot.logout()
        else:
            await ctx.send('No. I have eaten my fiber.')

def setup(bot):
    bot.add_cog(Bruh(bot))
    print('Miscellaneous module loaded.')
