import discord
from discord.ext import commands
import asyncio
import datetime
import random
from dateutil.relativedelta import relativedelta
from apex_legends import ApexLegends

ADMIN_ROLE = '547174572731006986', '228677568126124034'

def user_is_me(ctx):
    return ctx.message.author.id == "228017779511394304"

class Bruh:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, invoke_without_command=True)
	async def apex(self, ctx, player:str):
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
	async def psn(self, ctx, player:str):
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
	async def code(self, ctx):
		await self.bot.say('https://github.com/sirmammingtonham/yeeb')


	@commands.command(pass_context=True, no_pm=True)
	async def censor(self, ctx, *args, time:int=1):
		channel = ctx.message.channel
		if args is not None:
			user = ''
			for word in args:
				user += word
		elif args.isdigit():
			time = int(args)

		if time > 5:
			await self.bot.say('nah')
			return

		end = datetime.datetime.now() + datetime.timedelta(minutes=time)

		if user in [str(member) for member in ctx.message.server.members]:
			def check(message):
				return str(message.author) == user

			while datetime.datetime.now() < end:
				message = await self.bot.wait_for_message(channel=channel, check=check)
				await self.bot.delete_message(message)
				await self.bot.say(f'||{message.content}||')

		else:
			while datetime.datetime.now() < end:
				message = await self.bot.wait_for_message(channel=channel)
				await self.bot.delete_message(message)
				await self.bot.say(f'||{message.content}||')

	@commands.command(pass_context=True)
	async def invite(self, ctx):
		await self.bot.say('https://discordapp.com/oauth2/authorize?client_id=547156702626185230&scope=bot&permissions=8')

	@commands.command(pass_context=True)
	async def die(self, ctx):
		if user_is_me(ctx):
			await self.bot.logout()
		else:
			await self.bot.say('You cannot kill me, peasant.')

def setup(bot):
	bot.add_cog(Bruh(bot))