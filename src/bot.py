import discord
from discord.ext import commands
import asyncio
from itertools import cycle
from bs4 import BeautifulSoup
from mediawikiapi import MediaWikiAPI
from random import shuffle

with open("token.txt", "r") as f:
    TOKEN = f.read()
bot = commands.Bot(command_prefix = 'bruh ')
bot.remove_command('help')

# status = ['Minecraft', 'Roblox', 'Fortnite', 'on split screen']
extensions = ['bruh', 'music', 'events', 'card']

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

async def change_status(data):
    await bot.wait_until_ready()
    msgs = cycle(data)
    while not bot.is_closed:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(5)

if __name__ == '__main__':
    stati = headings('List of video games notable for negative reception')
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'{extension} cannot be loaded. [{e}]')
    bot.loop.create_task(change_status(stati))
    bot.run(TOKEN)