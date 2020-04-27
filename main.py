
import logging
from logging.handlers import RotatingFileHandler
import random
import sqlite3
import traceback
import time
from discord import utils
import datetime
import sys
import os
import hashlib
import asyncio
import aiohttp
from collections import Counter
import discord
from discord.ext import commands
from discord.utils import get
import loadconfig
import json
__version__ = '1.3.1'

description = ''' бот, разработанный с discord.py\n
                 Полный список всех команд доступен здесь: '''
bot = commands.Bot(command_prefix=get_prefix, description=description)
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '~'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, ident=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes,f,indent=4)

async def _randomGame():
    #Check games.py to change the list of "games" to be played
    while True:
        guildCount = len(bot.guilds)
        memberCount = len(list(bot.get_all_members()))
        randomGame = random.choice(loadconfig.__games__)
        await bot.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(guilds = guildCount, members = memberCount)))
        await asyncio.sleep(loadconfig.__gamesTimer__)

def _setupDatabase(db):
    with sqlite3.connect(db) as con:
        c = con.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS `reactions` (
                    	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    	`command`	TEXT NOT NULL,
                    	`url`	TEXT NOT NULL UNIQUE,
                    	`author`	TEXT
                    );''')
        con.commit()
        c.close()

@bot.event
async def on_ready():
    if bot.user.id == 606369466661732353:
        bot.dev = False
    else:
        bot.dev = False

    for guild in bot.guilds:
        for role in guild.roles:
            print(guild.name, role.id, role.name)

    print('Logged in as')
    print(f'Bot-Name: {bot.user.name}')
    print(f'Bot-ID: {bot.user.id}')
    print(f'Dev Mode: {bot.dev}')
    print(f'Discord Version: {discord.__version__}')
    print(f'Bot Version: {__version__}')
    bot.AppInfo = await bot.application_info()
    print(f'Owner: {bot.AppInfo.owner}')
    print('------')
    for cog in loadconfig.__cogs__:
        try:
            bot.load_extension(cog)
        except Exception:
            print(f'Couldn\'t load cog {cog}')
    bot.commands_used = Counter()
    bot.startTime = time.time()
    bot.botVersion = __version__
    bot.userAgentHeaders = {'User-Agent': f'linux:shinobu_discordbot:v{__version__} (by Der-Eddy)'}
    bot.gamesLoop = asyncio.ensure_future(_randomGame())
    _setupDatabase('reaction.db')

@bot.event
async def on_member_join(member):
    if member.guild.id == loadconfig.__botserverid__ and not bot.dev:
        if loadconfig.__greetmsg__ != 0:
            channel = member.guild.get_channel(loadconfig.__greetmsg__)
            emojis = [':wave:', ':congratulations:', ':wink:', ':cool:', ':tada:']
            await channel.send(random.choice(emojis)+ f'**Привествуем** тебя @{member.name} на сервере - **Gay Bar:Reborn**, **возми себе роли и прочитай правила(нет)**, для доступа в каналы с определенной тематикой.')
 
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if isinstance(message.channel, discord.DMChannel):
        await message.author.send(':x: Извините, но я не принимаю команды через прямые сообщения! Пожалуйста, используйте меня в канале `#флуд-ботинкам`!')
        return
    if bot.dev and not await bot.is_owner(message.author):
        return
    if bot.user.mentioned_in(message) and message.mention_everyone is False:
        if 'help' in message.content.lower():
            await message.channel.send('Полный список всех команд здесь: ')
        else:
            await message.add_reaction('👀') # :eyes:
    if 'loli' in message.clean_content.lower():
        await message.add_reaction('🍭') # :lollipop:
    if 'instagram.com' in message.clean_content.lower():
        await message.add_reaction('💩') # :poop:
    await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
    vipil = [
        f'@{member.name} слишком много выпил 🤪, пускай поспит, на утро все равно ничего не вспомнит 🤫',
        f'@{member.name} нажрался, не трогайте его',
        f'@{member.name} кажется мертв, го выебем его',
        f'@{member.name} жил без траха,  умер без траха',
        f'@{member.name} взорвал танцпол.. Среди пострадавших только он',
        ]
    if loadconfig.__greetmsg__ != 0:
        channel = member.guild.get_channel(loadconfig.__greetmsg__)
        await channel.send(random.choice(vipil))

@bot.event
async def on_error(event, *args, **kwargs):
    if bot.dev:
        traceback.print_exc()
    else:
        embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c) #Red
        embed.add_field(name='Event', value=event)
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.timestamp = datetime.datetime.utcnow()
        try:
            await bot.AppInfo.owner.send(embed=embed)
        except:
            pass

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.channel.send(':x: Этот Command был отключен')
    elif isinstance(error, commands.CommandInvokeError):
        if bot.dev:
            raise error
        else:
            embed = discord.Embed(title=':x: Command Error', colour=0x992d22) #Dark Red
            embed.add_field(name='Error', value=error)
            embed.add_field(name='Guild', value=ctx.guild)
            embed.add_field(name='Channel', value=ctx.channel)
            embed.add_field(name='User', value=ctx.author)
            embed.add_field(name='Message', value=ctx.message.clean_content)
            embed.timestamp = datetime.datetime.utcnow()
            try:
                await bot.AppInfo.owner.send(embed=embed)
            except:
                pass

@bot.command(hidden=True, aliases=['quit_backup'])
async def shutdown_backup(ctx):
    '''Запасной вариант, если mod cog не может загрузиться'''
    if await ctx.bot.is_owner(ctx.author):
        await ctx.send('**:ok:** Bye!')
        await bot.logout()
        sys.exit(0)
    else:
        await ctx.send('**:no_entry:** Ты не мой владелец бота!')

if __name__ == '__main__':
    bot.run(loadconfig.__token__)
