import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import random
import requests
from bs4 import BeautifulSoup
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
    async def clear_error(self, error, ctx):
        if isinstance(error, MissingPermissions):
            await ctx.send('You don\'t have the power, peasant.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def snap(self, ctx):
        channel = ctx.message.channel
        messages = []
        async for message in ctx.channel.history(after=datetime.now() - timedelta(days=14)):
            if not message.pinned and message.author.id == 547156702626185230:
                messages.append(message)
        random.shuffle(messages)
        await ctx.channel.delete_messages(messages[:len(messages)//2])
        await ctx.send('perfectly balanced\nhttps://media1.tenor.com/images/d89ba4e965cb9144c82348a1c234d425/tenor.gif?itemid=11793362', delete_after=30)

    @snap.error
    async def snap_error(self, error, ctx):
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
        words = open("../res/swearwords.txt").readlines()
        word = words[random.randrange(165)][:-1]
        await ctx.send(word)
        
    @commands.command(name='swearat', aliases=['insult'])
    async def swearat(self, ctx, name:str='', num_times:str=''):
        all_words = open("../res/swearwords.txt").readlines()
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
            if int(num_times) > 1000: num_times = 1000

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
        num_times = 1
        # Detect num_times argument. gotta check for positive and negative numbers
        if verbosify.isdigit(input_sentence.split()[0]):
            num_times = int(input_sentence.split()[0])

            # bruh don't try to break it bruh
            if num_times < 0 or num_times > 500:
                await ctx.send('bruh')
                return

            input_sentence = ' '.join(input_sentence.split()[1:])

        # run verbosify numerous times
        await verbosify.verbosify_ception(ctx, input_sentence, num_times)
        

    @commands.command()
    async def define(self, ctx, *args):
        await verbosify.get_definition(ctx, args)
    
    @commands.command(name='vernaculate', aliases=['conflobrinate'])
    async def vernaculate(self, ctx, *, video_game):
        if video_game: await ctx.send(f'<@&{748768498343346216}> it is {video_game} gamer time')
        else: await ctx.send(f'<@&{748768498343346216}> it is gamer time')

    @commands.command(name='fellas')
    async def fellas(self, ctx, *args):
        # first entry is emoji, second entry (if not None) is big photo version
        emojis = {'alex': ('<:alex:758937361001349150>', 'https://media.discordapp.net/attachments/270768847445950474/765453740319703050/alex.png'),
                  'justin': ('<:justin:758939166607933490>', 'https://media.discordapp.net/attachments/270768847445950474/765453747832619058/justin.png'),
                  'jacob': ('<:jacob:758937359928262676>', 'https://media.discordapp.net/attachments/270768847445950474/765453745240276992/jacob.png'),
                  'willu': ('<:willu:758937362821546026>', 'https://cdn.discordapp.com/attachments/425056372548173834/764762192208855050/willu.png'),
                  'willc': ('<:willc:758937363257753650>', 'https://cdn.discordapp.com/attachments/425056372548173834/764761954299805746/willcface.png'),
                  'craftyclashr': ('<:craftyclashr:758942144651722764>', 'https://media.discordapp.net/attachments/270768847445950474/765453740718686208/craftyclashr.png'),
                  'ethan': ('<:ethan:758956834882715648>', 'https://cdn.discordapp.com/attachments/425056372548173834/764762005839675392/ethanface.png'),
                  'boyu': ('<:boyu:765031756687605761>', 'https://cdn.discordapp.com/attachments/731662398196416573/765031191409065994/35DJIAAAAAElFTkSuQmCC.png')}
                #   'boyu': ('<:oldboyu:759184421030723646>', 'https://cdn.discordapp.com/attachments/425056372548173834/764762458710999071/unknown.png')}
        
        # chose a specific person
        if args and args[0] in emojis:
            person = emojis[args[0]]
            if person[1]: await ctx.send(person[1])
            else: await ctx.send(person[0])

        # didn't choose a specific person so send all emojis
        else:
            emoji_values = [emoji for emoji, link in list(emojis.values())]
            random.shuffle(emoji_values)
            await ctx.send(' '.join(emoji_values))

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
            'KILLJOY': 'The genius of Germany, Killjoy secures and defends key battlefield positions with a collection of traps, turrets, and mines. Each invention is primed to punish any assailant too dumb to back down.',
            'SKYE': 'Hailing from Australia, Skye and her band of beasts trailblaze the way through hostile territory. With her creations hampering the enemy, and her power to heal others, the team is strongests and safest by Skye\'s side.'
        }

        types = {
            'DUELIST': 'Duelists are self-sufficient fraggers who their team expects, through abilities and skills, to get high frags and seek out engagements first.',
            'INITIATOR': 'Initiators challenge angles by setting up their team to enter contested ground and push defenders away.',
            'CONTROLLER': 'Controllers are experts in slicing up dangerous territory to set their team up for success.',
            'SENTINEL': 'Sentinels are defensive experts who can lock down areas and watch flanks, both on attacker and defender rounds.'
        }

        abilities = {
            'SAGE': ['BARRIER ORB', 'SLOW ORB', 'HEALING ORB', 'RESURRECTION'],
            'SOVA': ['OWL DRONE', 'SHOCK BOLT', 'RECON BOLT', 'HUNTER\'S FURY'],
            'BREACH': ['AFTER SHOCK', 'FLASH POINT', 'FAULT LINE', 'ROLLING THUNDER'],
            'VIPER': ['SNAKE BITE', 'POISON CLOUD', 'TOXIC SCREEN', 'POISON PIT'],
            'BRIMSTONE': ['STIM BEACON', 'INCENDIARY', 'SKY SMOKE', 'ORBITAL STRIKE'],
            'CYPHER': ['TRIP WIRE', 'CYBER CAGE', 'SPY CAMERA', 'NEURAL THEFT'],
            'JETT': ['CLOUD BURST', 'UP DRAFT', 'TAIL WIND', 'BLADE STORM'],
            'OMEN': ['SHROUDED STEP', 'PARANOIA', 'DARK COVER', 'FROM THE SHADOWS'],
            'PHOENIX': ['BLAZE', 'CURVEBALL', 'HOT HANDS', 'RUN IT BACK'],
            'RAZE': ['BOOM BOT', 'BLAST PACK', 'PAINT SHELLS', 'SHOW STOPPER'],
            'REYNA': ['LEER', 'DEVOUR', 'DISMISS', 'EMPRESS'],
            'KILLJOY': ['ALARM BOT', 'NANO SWARM', 'TURRET', 'LOCKDOWN'],
            'SKYE': ['REGROWTH', 'GUIDING LIGHT', 'TRAILBLAZER', 'SEEKERS']
        }

        # abilities = {
        #     'BARRIER ORB': 'EQUIP a barrier orb. FIRE places a solid wall. ALT FIRE rotates the targeter.',
        #     'SLOW ORB': 'EQUIP a slowing orb. FIRE to throw a slowing orb forward that detonates upon landing, creating a lingering fielld that slows players caught inside of it.',
        #     'HEALING ORB': 'EQUIP a healing orb. FIRE with your crosshairs over a damaged ally to activate a heal-over-time on them. ALT FIRE while Sage is damaged to activate a self heal-over-time.'
        #     'RESURRECTION': 'EQUIP a resurrection ability. FIRE with your crosshairs placed over a dead ally to begin resurrecting them. After a brief channel, the ally will be brought back to life with full health.',

        #     'OWL DRONE': 'EQUIP an owl drone. FIRE to deploy and take control of movement of the drone. While in control of the drone, FIRE to shoot a marking dart. This dart will reveal the location of any player struck by the dart.',
        #     'SHOCK BOLT': 'EQUIP a bow with a shock bolt. FIRE to send the explosive bolt forward, detonating upon collision and damaging players nearby. HOLD FIRE to extend the range of the projectile. ALTERNATE FIRE to add up to two bounces to this arrow.',

        #     'AFTERSHOCK': 'EQUIP a fusion charge. FIRE the charge to set a slow-acting burst through the wall. The burst does heavy damage to anyone caught in its area.'
        # }
        
        # default values
        num_times = 1
        agent_text = random.choice(list(agents.values()))

        if len(args) == 1:
            # 1 word arg = arg agent, 1 time
            if args[0].upper() in agents: agent_text = agents[args[0].upper()]
            # or, chooose 5 random agents! added Jan 15 2021
            elif args[0].upper() == 'RANDOM':
                random_agent_list = random.sample(agents.keys(), 5)
                return await ctx.send(', '.join(random_agent_list))
             
            # 1 numerical arg = random agent, arg times
            elif verbosify.isdigit(args[0]): num_times = int(args[0])
        
        elif len(args) == 2:
            # check first arg as agent
            if args[0].upper() in agents: agent_text = agents[args[0].upper()]
            # check second arg as number
            if verbosify.isdigit(args[1]): num_times = int(args[1])

        # get 4 random abilities
        rand_abilities = []
        for _ in range(4):
            rand_agent = random.choice(list(agents.keys()))
            rand_ability = random.choice(abilities[rand_agent])
            rand_abilities.append(verbosify.verbosify(rand_ability).upper())

        rand_abilities = ', '.join(rand_abilities)

        output = agent_text + '\nABILITIES: ' + rand_abilities

        await verbosify.verbosify_ception(ctx, output, num_times)
        


         
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
    
    @commands.command()
    async def blur(self, ctx, *args):
        def _cv2_radial_blur(img):
            w, h = img.shape[:2]

            center_x = w / 2
            center_y = h / 2
            blur = 0.008
            iterations = 7

            growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
            shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x)*blur), (w, 1)).astype(np.float32)
            growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)
            shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y)*blur), (h, 1)).transpose().astype(np.float32)

            for i in range(iterations):
                tmp1 = cv2.remap(img, growMapx, growMapy, cv2.INTER_LINEAR)
                tmp2 = cv2.remap(img, shrinkMapx, shrinkMapy, cv2.INTER_LINEAR)
                img = cv2.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)
            
            return img
        
        def place_text(word, img):
            INITIAL_Y = [None,250,210,170,130]
            words = word.split()
            y = 270 - 35*(len(words)-1) # initial y
            
            for word in words:
                cv2.putText(img, word, (500,y), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,0), 3)
                y += 70
            
            return img

            formatted = word.replace(' ', '\n')
            print(formatted)

            l = len(word.split())
            if l < 5: return (formatted, (500,250 - 50*(l-1)))
            else: return (formatted, (500,50))

        def _radically_blur(f, word):
            # place image on white background
            overlay = cv2.imdecode(np.fromstring(f.read(), np.uint8), 1)
            overlay = cv2.resize(overlay, (400, 300))
            img = np.full((500,800,3), 255, np.uint8)
            img[100:400, 50:450] = overlay

            # put text on image
            img = place_text(word, img)

            # blur image
            img = _cv2_radial_blur(img)

            # return
            _, buffer = cv2.imencode(".jpg", img)
            return buffer
        

        # get query keyword and word to display on image
        word = ' '.join(args)
        query = '-'.join(args)
        i = word.find(' as ')
        if i != -1:
            query = word[:i].replace(' ', '-')
            word = word[i+4:]

        print(query, word)

        r = requests.get("https://source.unsplash.com/featured/?{}".format(query))

        if r.status_code == 200:
            f = BytesIO(r.content)
            blurred = _radically_blur(f, word)
            await ctx.send(file=discord.File(BytesIO(blurred), 'blur_boi.jpg'))
        else:
            await ctx.send("this big bruh moment is a big bruh moment for sure")



    @commands.command(name='cum', aliases=['nut'])
    async def cum(self, ctx):
        await ctx.send("https://i.pinimg.com/736x/38/e9/57/38e957bb23e73d3759dda419cece5bc0.jpg")

    @commands.command()
    async def korra(self, ctx):
        will_cookie = 'https://media.discordapp.net/attachments/661185720211341312/739759077302861875/image0.jpg'
        links = {
            'https://cdn.discordapp.com/attachments/661185720211341312/733258810713571378/Screenshot_20200716-0248022.png': 7,
            'https://cdn.discordapp.com/attachments/661185720211341312/739748973597818880/unknown.png': 8,
            'https://cdn.discordapp.com/attachments/661185720211341312/738668566793945098/unknown.png': 6,
            'https://cdn.discordapp.com/attachments/661185720211341312/737209307900149811/unknown.png': 3,
            'https://cdn.discordapp.com/attachments/661185720211341312/737203525330665502/unknown.png': 6,
            'https://cdn.discordapp.com/attachments/661185720211341312/737203457781530744/unknown.png': 8,
            'https://cdn.discordapp.com/attachments/661185720211341312/737203345894408232/unknown.png': 8,
            'https://cdn.discordapp.com/attachments/661185720211341312/736516684663226398/unknown.png': 5,
            'https://cdn.discordapp.com/attachments/661185720211341312/736511129538265128/unknown.png': 6,
            'https://media.discordapp.net/attachments/661185720211341312/741580668592586783/unknown.png': 3,
            'https://media.discordapp.net/attachments/661185720211341312/741950835348471909/unknown.png': 8,
            'https://media.discordapp.net/attachments/661185720211341312/741950996279984138/unknown.png': 6,
            'https://media.discordapp.net/attachments/661185720211341312/741951109631049748/unknown.png': 6,
            'https://media.discordapp.net/attachments/661185720211341312/741952947122077696/unknown.png': 7,
            'https://media.discordapp.net/attachments/661185720211341312/741956214157475860/unknown.png': 8,
            'https://cdn.discordapp.com/attachments/661185720211341312/744820991078957076/unknown.png': 14,
            'https://cdn.discordapp.com/attachments/661185720211341312/744822933897347122/unknown.png': 6,
            'https://cdn.discordapp.com/attachments/425056372548173834/744426038238380032/unknown.png': 5,
            'https://media.discordapp.net/attachments/425056372548173834/745186855141638154/unknown.png': 16
        }

        if random.randrange(int(len(links)/1.5)) == 0: await ctx.send(will_cookie)
        else: await ctx.send(random.choices(list(links.keys()), weights=links.values(), k=1)[0], delete_after=30)

        
    @commands.command(name='shityourpants', aliases=['shitthinebritches', 'poopyourself'])
    async def shityourpants(self, ctx):
        if user_is_bot_contributor(ctx):
            await self.bot.logout()
        else:
            await ctx.send('No. I have eaten my fiber.')
    
    @commands.command(name='yo')
    async def yo_mama(self, ctx):
        response = requests.get('https://www.laughfactory.com/jokes/yo-momma-jokes')
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find_all('div', {'class': 'joke-text'})
        jokes = [joke.find('p').text.strip() for joke in div]
        await ctx.send(random.choice(jokes))
    
    @commands.command(name='delete', aliases=['d'])
    async def delete(self, ctx, *args):
        msg_history = await ctx.channel.history(limit=2).flatten()
        await msg_history[1].delete()

def setup(bot):
    bot.add_cog(Bruh(bot))
    print('Miscellaneous module loaded.')
