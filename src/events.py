import discord
import random
from discord.ext import commands
import asyncio
from itertools import cycle
from bs4 import BeautifulSoup
from mediawikiapi import MediaWikiAPI
from random import shuffle

ligma = [' balls\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg', ' dick\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
         ' deez nuts\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg', ' dick fit in yo mouth son?\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
         ' ass, lil bitch\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
        ]

def wikitable(page):
    """
    Exports a Wikipedia table parsed by BeautifulSoup. Deals with spanning: 
    multirow and multicolumn should format as expected. 
    """
    mediawikiapi = MediaWikiAPI()
    page = mediawikiapi.page(page)
    soup = BeautifulSoup(page.html(), 'html.parser')
    rows=table.findAll("tr")
    ncols=max([len(r.findAll(['th','td'])) for r in rows])

    # preallocate table structure
    # (this is required because we need to move forward in the table
    # structure once we've found a row span)
    data=[]
    for i in range(nrows):
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

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(change_status(self.bot, headings('List of video games notable for negative reception')))
        print('it seems to be working...')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        text = message.content.lower()
        if 'what\'s' in text or 'whats' in text:
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

        if text.startswith('i\'m') or text.startswith('im'):
            im = 'i\'m' if 'i\'m' in text else 'im'
            text = text[text.find(im) + len(im)+1:]
            await message.channel.send('Hi ' + text + ', I\'m yeeb bot', delete_after=30)

def setup(bot):
    bot.add_cog(Events(bot))
    print('Event module loaded.')