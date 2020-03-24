import datetime
import asyncio
import aiohttp
import discord
from discord.ext import commands
import loadconfig

class mod(commands.Cog):
    '''Удобные команды для администраторов и модераторов'''

    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(mod(bot))
