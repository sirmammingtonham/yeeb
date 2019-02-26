import discord
from discord.ext import commands
import youtube_dl
import asyncio
from itertools import cycle
import datetime
from dateutil.relativedelta import relativedelta
import urllib.request
import random

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')
    
TOKEN = 'NTQ3MTU2NzAyNjI2MTg1MjMw.D0yrZw.C57ut2uYOCcTLc3ijW_DgvNG-1Y'
ADMIN_ROLE = '547174572731006986', '228677568126124034'
beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
status = ['Minecraft', 'Roblox', 'Fortnite', 'at the same time...']
jojos = ['https://www.youtube.com/watch?v=tHAGig0Mq6o', 'https://www.youtube.com/watch?v=P-3GOo_nWoc&t=38s', 
		 'https://www.youtube.com/watch?v=ITMjAeWz5hk', 'https://www.youtube.com/watch?v=cPCLFtxpadE',
		 'https://www.youtube.com/watch?v=NFjE5A4UAJI', 'https://www.youtube.com/watch?v=So54Khf7bB8',
		 'https://www.youtube.com/watch?v=J69VjA6wUQc',
		]
queues, players = {}, {}
#create_ytdl_player(url=self.url, ytdl_options=self.ytdl_format_options, before_options=beforeArgs)
bot = commands.Bot(command_prefix = 'bruh ')
bot.remove_command('help')

def user_is_me(ctx):
    return ctx.message.author.id == "228017779511394304"

def check_queue(id):
	if queues[id] != []:
		player = queues[id].pop(0)
		players[id] = player
		player.start()
	else:
		del players[id]

async def change_status():
	await bot.wait_until_ready()
	msgs = cycle(status)
	while not bot.is_closed:
		current_status = next(msgs)
		await bot.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(5)

@bot.event
async def on_ready():
	print('it seems to be working...')

@bot.event
async def on_message(message):
	if 'what\'s' in message.content.lower():
		num = random.randint(1,5)
		if message.content[7:] == 'ligma' or num == 1:
			await bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + ' balls\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg')
		elif message.content[7:] == 'kisma' or num == 2:
			await bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + ' dick\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg')
		elif message.content[7:] == 'bofa' or num == 3:
			await bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + ' deez nuts\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg')
		elif message.content[7:] == 'candice' or num == 4:
			await bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + ' dick fit in yo mouth son?\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg')
		elif message.content[7:] == 'fugma' or num == 5:
			await bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + ' ass, lil bitch\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg')
	await bot.process_commands(message)

@bot.command(pass_context=True)
async def help(ctx):
	await bot.send_message(ctx.message.author, 'bet')

@bot.command(pass_context=True)
async def cardgame(ctx):
	await bot.send_message(ctx.message.author, 'bet')

@bot.command(pass_context=True)
async def clear(ctx, amount=100):
	channel = ctx.message.channel
	messages = []
	async for message in bot.logs_from(channel, limit=int(amount)):
		messages.append(message)
	await bot.delete_messages(messages)
	await bot.say('I\'m still logging all your data lol')
	await asyncio.sleep(10)
	async for message in bot.logs_from(channel, limit=int(1)):
		await bot.delete_messages([message])

@bot.command(pass_context=True)
async def snap(ctx):
	channel = ctx.message.channel
	messages = []
	async for message in bot.logs_from(channel, limit=int(100)):
		messages.append(message)
	random.shuffle(messages)
	await bot.delete_messages(messages[:len(messages)//2])
	await bot.say('perfectly balanced\nhttps://media1.tenor.com/images/d89ba4e965cb9144c82348a1c234d425/tenor.gif?itemid=11793362')

@bot.command(pass_context=True)
async def play(ctx, url):
	global queue
	channel = ctx.message.author.voice.voice_channel
	try:
		await bot.join_voice_channel(channel)
	except:
		print('already in voice channel')

	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

	if server.id not in players:
		players[server.id] = player
		player.start()
	else:
		if server.id in queues:
			queues[server.id].append(player)
		else:
			queues[server.id] = [player]
	
	await bot.say('Queued:\n' + url)

@bot.command(pass_context=True)
async def onjah(ctx):
	channel = ctx.message.author.voice.voice_channel
	try:
		await bot.join_voice_channel(channel)
	except:
		pass
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	if server.id not in players:
		player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=fGZb5SpRCi0')
		players[server.id] = player
		player.start()
		await bot.say('https://www.pngkey.com/png/detail/486-4869960_xxxtentacion-face-png-xxxtentacion-meme-face.png')

@bot.command(pass_context=True)
async def this(ctx, *args):
	check = ''
	for word in args:
		check += word
	if check == 'issosad':
		word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
		response = urllib.request.urlopen(word_url)
		long_txt = response.read().decode()
		words = long_txt.splitlines()
		number = random.randint(1, len(words)-1)
		if number % 2 == 0:
			await bot.say(f'can we hit {number} {words[number]}')
		else:
			await bot.say(f'can we hit {number} {words[number]} {words[random.randint(1,10000)]}')

@bot.command(pass_context=True)
async def moment(ctx):
	channel = ctx.message.author.voice.voice_channel
	try:
		await bot.join_voice_channel(channel)
	except:
		pass
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=2ZIpFytCSVc')
	players[server.id] = player
	player.start()

@bot.command(pass_context=True)
async def go(ctx, *args):
	check = ''
	for word in args:
		check += word
	if check == 'sickomode':
		channel = ctx.message.author.voice.voice_channel
		try:
			await bot.join_voice_channel(channel)
		except:
			pass
		server = ctx.message.server
		voice_client = bot.voice_client_in(server)
		if server.id not in players:
			player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=qMc6xlZaxYA')
			players[server.id] = player
			player.start()
			await bot.say('https://media1.giphy.com/media/1oE3Ee4299mmXN8OYb/source.gif')

@bot.command(pass_context=True)
async def jojo(ctx):
	channel = ctx.message.author.voice.voice_channel
	try:
		await bot.join_voice_channel(channel)
	except:
		pass
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	if server.id not in players:
		url = jojos[random.randint(0,len(jojos)-1)]
		player = await voice_client.create_ytdl_player(url)
		players[server.id] = player
		player.start()

@bot.command(pass_context=True)
async def finnasmash(ctx):
	channel = ctx.message.author.voice.voice_channel
	try:
		await bot.join_voice_channel(channel)
	except:
		pass
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	if server.id not in players:
		player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=EhgDibw7vB4')
		players[server.id] = player
		player.start()

@bot.command(pass_context=True)
async def mutethisbitch(ctx):
	pass

@bot.command(pass_context=True)
async def leave(ctx):
	global queues
	global players
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	await voice_client.disconnect()
	queues = {}
	players = {}

@bot.command(pass_context=True)
async def spam(ctx, *args):
	if user_is_me(ctx):
		for _ in range(int(args[-1])):
			output = ''
			for word in args[:-1]:
				output += word + ' '
			await bot.say(output)
	else:
		await bot.say('You don\'t have the power, peasant.')

@bot.command(pass_context=True)
async def thatsprettycringe(ctx):
	await bot.say('https://i.ytimg.com/vi/ZtFteHYmxuQ/hqdefault.jpg')

@bot.command(pass_context=True)
async def howlong(ctx):
	td = relativedelta(datetime.datetime(2020, 12, 11), datetime.datetime.now())
	await bot.say(f'Bobby Shmurda will be released in {td.years} years, {td.months} months, {td.days} days, {td.hours} hours, {td.minutes} minutes, and {td.seconds} seconds.')


@bot.command(pass_context=True)
async def die(ctx):
	if user_is_me(ctx):
		await bot.logout()
	else:
		await bot.say('You cannot kill me, peasant.')


bot.loop.create_task(change_status())
bot.run(TOKEN)