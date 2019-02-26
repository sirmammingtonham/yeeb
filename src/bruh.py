import discord
from discord.ext import commands
import asyncio
import datetime
import urllib.request
import random
from dateutil.relativedelta import relativedelta
from mediawikiapi import MediaWikiAPI
from apex_legends import ApexLegends

ADMIN_ROLE = '547174572731006986', '228677568126124034'

def user_is_me(ctx):
    return ctx.message.author.id == "228017779511394304"

class Bruh:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, invoke_without_command=True)
	async def apex(self, ctx, player : str):
		if ctx.invoked_subcommand is None:
			apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
			try:
				player = apex.player(player)
			except:
				await self.bot.say('Player not found')
				return
			embed = discord.Embed(
				 colour = discord.Colour.blue()
				 )
			embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
			embed.set_thumbnail(url=player.legends[0].icon)
			embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
			embed.add_field(name='Level:', value=player.level, inline=False)
			# for legend in player.legends:
			# 	embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
			for a in dir(player.legends[0]):
				if a == 'damage' or 'kills' in a:
					name = a + ':'
					embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
			await self.bot.say(embed=embed)

	@apex.command(pass_context=True)
	async def xbox(self, ctx, *args):
		apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
		try:
			name = ''
			for word in args:
				name += word + ' '
			player = apex.player(name, plat=1)
		except:
			await self.bot.say('Player not found')
			return
		embed = discord.Embed(
			 colour = discord.Colour.blue()
			 )
		embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
		embed.set_thumbnail(url=player.legends[0].icon)
		embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
		embed.add_field(name='Level:', value=player.level, inline=False)
		# for legend in player.legends:
		# 	embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
		for a in dir(player.legends[0]):
			if a == 'damage' or 'kills' in a:
				name = a + ':'
				embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
		await self.bot.say(embed=embed)

	@apex.command(pass_context=True)
	async def psn(self, ctx, player : str):
		apex = ApexLegends("af6873a1-ef18-4ea4-aced-143ba5b6eb5d")
		try:
			player = apex.player(player, plat=2)
		except:
			await self.bot.say('Player not found')
			return
		embed = discord.Embed(
			 colour = discord.Colour.blue()
			 )
		embed.set_footer(text='the stat tracking right now is ass so I can only show damage and kills if you have the banner')
		embed.set_thumbnail(url=player.legends[0].icon)
		embed.set_author(name=player.username + ' | ' + player.legends[0].legend_name, icon_url='https://cdn.gearnuke.com/wp-content/uploads/2019/02/apex-legends-logo-768x432.jpg')
		embed.add_field(name='Level:', value=player.level, inline=False)
		# for legend in player.legends:
		# 	embed.add_field(name=legend.legend_name, value='Stats:', inline=False)
		for a in dir(player.legends[0]):
			if a == 'damage' or 'kills' in a:
				name = a + ':'
				embed.add_field(name=name.capitalize(), value=player.legends[0].__dict__[a], inline=True)
		await self.bot.say(embed=embed)

	@commands.command(pass_context=True)
	async def help(self, ctx):
		await self.bot.send_message(ctx.message.author, 'bet')

	@commands.command(pass_context=True)
	async def clear(self, ctx, amount=100):
		if user_is_me(ctx):
			channel = ctx.message.channel
			messages = []
			async for message in self.bot.logs_from(channel, limit=int(amount)):
				messages.append(message)
			await self.bot.delete_messages(messages)
			await self.bot.say('I\'m still logging all your data lol')
			await asyncio.sleep(10)
			async for message in self.bot.logs_from(channel, limit=int(1)):
				await self.bot.delete_messages([message])
		else:
			await self.bot.say('You don\'t have the power, peasant.')

	@commands.command(pass_context=True)
	async def snap(self, ctx):
		channel = ctx.message.channel
		messages = []
		async for message in self.bot.logs_from(channel, limit=int(100)):
			messages.append(message)
		random.shuffle(messages)
		await self.bot.delete_messages(messages[:len(messages)//2])
		await self.bot.say('perfectly balanced\nhttps://media1.tenor.com/images/d89ba4e965cb9144c82348a1c234d425/tenor.gif?itemid=11793362')

	@commands.command(pass_context=True)
	async def this(self, ctx, *args):
		check = ''
		for word in args:
			check += word
		if check == '':
			mediawikiapi = MediaWikiAPI()
			await self.bot.say(f'this is so {mediawikiapi.random()}, can we hit {random.randint(0,10000000)} {mediawikiapi.random()}')
		elif check == 'issosad':
			word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
			response = urllib.request.urlopen(word_url)
			long_txt = response.read().decode()
			words = long_txt.splitlines()
			number = random.randint(1, len(words)-1)
			if number % 2 == 0:
				await self.bot.say(f'can we hit {number} {words[number]}')
			else:
				await self.bot.say(f'can we hit {number} {words[number]} {words[random.randint(1,10000)]}')


	@commands.command(pass_context=True)
	async def finnasmash(self, ctx):
		await self.bot.say('This command has changed, you absolute knob. Try ```py\nbruh finna smash\n``` instead.')

	@commands.command(pass_context=True)
	async def spam(self, ctx, *args):
		if user_is_me(ctx):
			for _ in range(int(args[-1])):
				output = ''
				for word in args[:-1]:
					output += word + ' '
				await self.bot.say(output)
		else:
			await self.bot.say('You don\'t have the power, peasant.')

	@commands.command(pass_context=True)
	async def thatsprettycringe(self, ctx):
		await self.bot.say('https://i.ytimg.com/vi/ZtFteHYmxuQ/hqdefault.jpg')

	@commands.command(pass_context=True)
	async def howlong(self, ctx):
		td = relativedelta(datetime.datetime(2020, 12, 11), datetime.datetime.now())
		await self.bot.say(f'Bobby Shmurda will be released in {td.years} years, {td.months} months, {td.days} days, {td.hours} hours, {td.minutes} minutes, and {td.seconds} seconds.')

	@commands.command(pass_context=True)
	async def die(self, ctx):
		if user_is_me(ctx):
			await self.bot.logout()
		else:
			await self.bot.say('You cannot kill me, peasant.')

def setup(bot):
	bot.add_cog(Bruh(bot))