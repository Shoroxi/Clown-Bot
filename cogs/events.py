import discord
import random
import logging
from logging.handlers import RotatingFileHandler
import sqlite3
import traceback
import time
from discord import utils
import datetime
import sys
import os
import hashlib
import aiohttp
from collections import Counter
import json
import asyncio
from discord.ext import commands
from discord.utils import get
from concurrent import futures
from urllib.parse import urlparse
import loadconfig
bot = commands.Bot(command_prefix=loadconfig.__prefix__)
class EventsCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
def setup(bot):
    bot.add_cog(EventsCog(bot))
