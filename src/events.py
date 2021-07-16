import re
import discord
import random
from discord.ext import commands
import asyncio
from itertools import cycle
from bs4 import BeautifulSoup
from mediawikiapi import MediaWikiAPI
import random
from discord.utils import get

from PIL import Image, ImageDraw, ImageSequence, ImageFile, ImageFont
import io
ImageFile.LOAD_TRUNCATED_IMAGES = True

ligma = [' balls\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg', ' dick\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
         ' deez nuts\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg', ' dick fit in yo mouth son?\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
         ' ass, lil bitch\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
        ]

ihardlyknowher = open('../res/erwords.txt', 'r').read().split()


def wikitable(page):
    """
    Exports a Wikipedia table parsed by BeautifulSoup. Deals with spanning: 
    multirow and multicolumn should format as expected. 
    """
    mediawikiapi = MediaWikiAPI()
    page = mediawikiapi.page(page)
    soup = BeautifulSoup(page.html(), 'html.parser')
    rows = soup.findAll("tr")
    ncols = max([len(r.findAll(['th','td'])) for r in rows])

    # preallocate table structure
    # (this is required because we need to move forward in the table
    # structure once we've found a row span)
    data=[]
    for i in range(len(rows)):
        rowD=[]
        for j in range(ncols):
            rowD.append('')
        data.append(rowD)

    # fill the table with data:
    # move across cells and use span to fill extra cells
    for i,row in enumerate(rows):    
        cells = row.findAll(["td","th"])
        for j,cell in enumerate(cells):        
            cspan=int(cell.get('colspan',1))
            rspan=int(cell.get('rowspan',1))
            l = 0
            for k in range(rspan):
                # Shifts to the first empty cell of this row
                # Avoid replacing previously insterted content
                while data[i+k][j+l]:
                    l+=1
                for m in range(cspan):
                    data[i+k][j+l+m]+=cell.text.strip("\n")
    return data

def headings(page):
    mediawikiapi = MediaWikiAPI()
    page = mediawikiapi.page(page)
    soup = BeautifulSoup(page.html(), 'html.parser')
    data = []
    for headlines in soup.find_all("h3"):
        data.append(headlines.text.strip()[:headlines.text.strip().find(' (')])
    return data

async def change_status(bot, data):
    await bot.wait_until_ready()
    msgs = cycle(data)
    while not bot.is_closed():
        current_status = next(msgs)
        await bot.change_presence(activity=discord.Game(name=current_status))
        await asyncio.sleep(5)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignore_servers = [669396255260016642]

    async def _crabby(self, message, text):
        W, H = (352,200)
        im = Image.open('../images/crabrave.gif')

        frames = []
        # Loop over each frame in the animated image
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert('RGB')
            
            # Draw the text on the frame
            d = ImageDraw.Draw(frame)
            color = '#fff'
            
            # draw message
            myFont = ImageFont.truetype("../res/GILLSANS.TTF", 42)
            top_msg = text[:-8].upper()
            w, h = d.textsize(top_msg, font=myFont)
            d.text(((W-w)/2, 50), top_msg, font=myFont, fill=color)
            
            w, h = d.textsize('IS GONE', font=myFont)
            d.text(((W-w)/2, 100), 'IS GONE', font=myFont, fill=color)
            
            # draw line
            d.line((int(W*0.15),H/2, int(W*0.85),H/2), fill=color)
            
            del d
            
            # save
            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)

            # Then append the single frame image to a list of frames
            frames.append(frame)
            
        # save frames as GIF
        f = io.BytesIO()
        frames[0].save(f, format="GIF", save_all=True, append_images=frames[1:])
        f.seek(0)
        await message.channel.send(file=discord.File(f, 'obama.gif'), delete_after=120)
    
    async def _ligma(self, message, text):
        what = 'what\'s' if 'what\'s' in text else 'whats'
        text = text[text.find(what) + len(what)+1:]

        if text == 'ligma':
            await message.channel.send(text + ligma[0], delete_after=30)
        elif text == 'kisma':
            await message.channel.send(text + ligma[1], delete_after=30)
        elif text == 'bofa':
            await message.channel.send(text + ligma[2], delete_after=30)
        elif text == 'candice':
            await message.channel.send(text + ligma[3], delete_after=30)
        elif text == 'fugma':
            await message.channel.send(text + ligma[4], delete_after=30)
        else:
            await message.channel.send(text + ligma[random.randint(0,4)], delete_after=30)
    
    async def _dad(self, message, text):
        im = 'i\'m' if 'i\'m' in text else 'im' if 'im' in text else 'i am'
        word = text[text.find(im) + len(im)+1:]
        await message.channel.send('Hi ' + word + ', I\'m yeeb bot', delete_after=15)
    
    async def _her(self, message, text):
        if message.author.id == self.bot.user.id:
           return
        
        for word in text.split():
            if word in ihardlyknowher and random.random() < 0.33:
                return await message.channel.send(word.capitalize() + '? I hardly know her.', delete_after=15)

        # matches = re.findall(r'(\w*er|\w*or)\b', text)  # regex matches all words that end in 'er' or 'or'

        # for match in matches:
        #     # if random.random() < 0.33:
        #     await message.channel.send(match.capitalize() + '? I hardly know her.', delete_after=15)
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(change_status(self.bot, headings('List of video games notable for negative reception')))
        print('it seems to be working...')

    @commands.Cog.listener()
    async def on_message(self, message):

        text = message.content.lower()

        if 'is gone' in text:
            await self._crabby(message, text)
        
        # dont want the other commands spamming important servers
        if message.guild.id in self.ignore_servers:
            return
        
        if 'what\'s' in text or 'whats' in text:
            await self._ligma(message, text)

        if text.startswith('i\'m') or text.startswith('im') or text.startswith('i am'):
            await self._dad(message, text)
        
        if 'er' in text or 'or' in text:
            await self._her(message, text)
    

    # if someone reacts, yeebbot will add that same reaction
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await reaction.message.add_reaction(reaction)
    
    # (or remove it if user removes their reaction)
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # get yeebbot member object
        yeebbot = reaction.message.guild.get_member(547156702626185230)
        await reaction.message.remove_reaction(reaction, yeebbot)
    
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if(member.guild.id == 319277087401705482):
            role_id = 428410186072588289
            fellas_role = get(member.guild.roles, id=role_id)
            await member.edit(nick = 'sample text', roles = [fellas_role])
                 

def setup(bot):
    bot.add_cog(Events(bot))
    print('Event module loaded.')
