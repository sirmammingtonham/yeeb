from discord.ext import commands


class YeebBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_command('help')

    async def setup_hook(self):
        extensions = [
            'src.bruh', 
            'src.events', 
            'src.card', 
            'src.meem', 
            'src.music',
            # 'src.experimental.speed'
        ]
        for extension in extensions:
            await self.load_extension(extension)