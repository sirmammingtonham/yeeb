import discord
import random

class Events:
	def __init__(self, bot):
		self.bot = bot
		self.ligma = [' balls\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg', ' dick\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
					  ' deez nuts\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg', ' dick fit in yo mouth son?\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg',
					  ' ass, lil bitch\nhttps://i.ytimg.com/vi/ylYqTYJ8vbs/maxresdefault.jpg']

	async def on_ready(self):
		print('it seems to be working...')

	async def on_message(self, message):
		if 'what\'s' in message.content.lower():
			if message.content[message.content.lower().find('what\'s')+7:] == 'ligma':
				await self.bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + self.ligma[0])
			elif message.content[message.content.lower().find('what\'s')+7:] == 'kisma':
				await self.bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + self.ligma[1])
			elif message.content[message.content.lower().find('what\'s')+7:] == 'bofa':
				await self.bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + self.ligma[2])
			elif message.content[message.content.lower().find('what\'s')+7:] == 'candice':
				await self.bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + self.ligma[3])
			elif message.content[message.content.lower().find('what\'s')+7:] == 'fugma':
				await self.bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + self.ligma[4])
			else:
				await self.bot.send_message(message.channel, message.content[message.content.lower().find('what\'s')+7:] + self.ligma[random.randint(0,4)])
		if message.content.lower().startswith('i\'m'):
			await self.bot.send_message(message.channel, 'Hi ' + message.content[message.content.lower().find('i\'m')+4:] + ', I\'m yeeb bot')
		# await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(Events(bot))