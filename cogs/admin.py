import sys
import os
import random
import discord
import asyncio
import aiohttp
import time
from discord.ext import commands
import loadconfig
from datetime import datetime as d

gay = ['100%! да ты бомба', '99% -_-.. а где уй в жопе?', '93%', '91%',  '89%',  '87%',  '85%',  '83%','81%', '79%', '77%', '75%', '73%', '71%', '69%', '67%', '65%', '63%', '60%', '59%', '57%',  '55%',  '53%', '51%', '50% истинный баланс', '49% а дотянуть не мог а?', '48%а дотянуть не мог а?', '47%', '45%', '43%', '42%', '40%', '38%', '36%', '34%', '32%',  '30%', '28%',  '26%',  '24%', '22%',  '20%',  '18%',  '16%',  '14%',  '12%',  '10%', '9% ты на грани', '8% ты на грани', '7% ты на грани', '6% ты на грани', '5% ты на грани', '4% ты на грани', '3% ты на грани', '2% ты на грани', '1% ты на грани', '0% кажется тебе здесь не место']
colors = {
  'DEFAULT': 0x000000,
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'GREY': 0x95A5A6,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_GREY': 0x979C9F,
  'DARKER_GREY': 0x7F8C8D,
  'LIGHT_GREY': 0xBCC0C0,
  'DARK_NAVY': 0x2C3E50,
  'BLURPLE': 0x7289DA,
  'GREYPLE': 0x99AAB5,
  'DARK_BUT_NOT_BLACK': 0x2C2F33,
  'NOT_QUITE_BLACK': 0x23272A
}

class admin(commands.Cog):
    '''Команды для бота Admin'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    @commands.command(aliases=['пинг'], hidden=True)
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(aliases=['сдох'], hidden=True)
    async def shutdown(self, ctx):
        '''Отключает меня :( (BOT OWNER ONLY)'''
        await ctx.send('**:ok:** До связи!')
        #self.bot.gamesLoop.cancel()
        await self.bot.logout()
        sys.exit(0)

    @commands.command(hidden=True)
    async def restart(self, ctx):
        '''Перезапускает меня (BOT OWNER ONLY)'''
        await ctx.send('**:ok:** Сейчас приду!')
        await self.bot.logout()
        sys.exit(6)

    @commands.command(aliases=['аватар'], hidden=True)
    async def avatar(self, ctx, url: str):
        '''Устанавливает новый аватар (BOT OWNER ONLY)'''
        tempAvaFile = 'tempAva.png'
        async with aiohttp.get(''.join(url)) as img:
            with open(tempAvaFile, 'wb') as f:
                f.write(await img.read())
        f = discord.File(tempAvaFile)
        await self.bot.edit_profile(avatar=f.read())
        os.remove(tempAvaFile)
        asyncio.sleep(2)
        await ctx.send('**:ok:** Мой новый аватар!\n %s' % self.bot.user.avatar_url)

    @commands.command(hidden=True, aliases=['игра'])
    async def changegame(self, ctx, gameType: str, *, gameName: str):
        '''Изменение текущей игры (BOT OWNER ONLY)'''
        gameType = gameType.lower()
        if gameType == 'playing':
            type = discord.Activity.playing
        elif gameType == 'watching':
            type = discord.Activity.watching
        elif gameType == 'listening':
            type = discord.Activity.listening
        elif gameType == 'streaming':
            type = discord.Activity.streaming
        guildsCount = len(self.bot.guilds)
        memberCount = len(list(self.bot.get_all_members()))
        gameName = gameName.format(guilds = guildsCount, members = memberCount)
        await self.bot.change_presence(activity=discord.Activity(type=type, name=gameName))
        await ctx.send(f'**:ok:** Изменить игру на: {gameType} **{gameName}**')

    @commands.command(hidden=True, aliases=['статус'])
    async def changestatus(self, ctx, status: str):
        '''Изменение онлайн-статуса бота (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus)
        await ctx.send(f'**:ok:** Изменить статус на: **{discordStatus}**')

    @commands.command(aliases=['%гея']) #пинг
    async def howgay(self,ctx):
        await ctx.send(random.choice(gay))

    @commands.command(aliases=['сумма']) #добавление
    async def add(self, ctx, a: float, b: float):
            await ctx.send(f'Сумма **{a}** и **{b}**  равна  **{a+b}**')

    @commands.command(aliases=['произведение']) #умножение
    async def multiply(self, ctx, a: float, b: float, ):
            await ctx.send(f'Произведение **{a}** на **{b}**  равна  **{a*b}**')

    @commands.command(aliases=['деление']) #деление
    async def half(self, ctx, a: float, b: float, ):
        try:
            if b == 0:
                await ctx.send("делить на 0 нельзя, ебалоид")
            else:
                await ctx.send(f'Деление **{a}** на **{b}**  равна  **{a/b}**')
        except:
            if isinstance(commands.MessageConverter):
                await ctx.author.send('This command cannot be used in private messages.')

            
    @commands.command(hidden=True,
        name='embed',
        description='The embed command', )
    async def embed_command(self, ctx):

        # Define a check function that validates the message received by the bot
        def check(ms):
            # Look for the message sent in the same channel where the command was used
            # As well as by the user who used the command.
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        # First ask the user for the title
        await ctx.send(content='Какое название будет?')

        # Wait for a response and get the title
        msg = await self.bot.wait_for('message', check=check)
        title = msg.content # Set the title

        # Next, ask for the content
        await ctx.send(content='Какое описание?')
        msg = await self.bot.wait_for('message', check=check)
        desc = msg.content

        # Finally make the embed and send it
        msg = await ctx.send(content='Теперь генерируем embed...')

        color_list = [c for c in colors.values()]
        # Convert the colors into a list
        # To be able to use random.choice on it

        embed = discord.Embed(
            title=title,
            description=desc,
            color=random.choice(color_list)
        )
        # Also set the thumbnail to be the bot's pfp
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        # Also set the embed author to the command user
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )

        await msg.edit(
            embed=embed,
            content=None
        )
        # Editing the message
        # We have to specify the content to be 'None' here
        # Since we don't want it to stay to 'Now generating embed...'

        return

    @commands.command(hidden=True)
    async def name(self, ctx, name: str):
        '''Изменение глобального имени бота (BOT OWNER ONLY)'''
        await self.bot.edit_profile(username=name)
        msg = f':ok: Измените мое имя на: **{name}**'
        await ctx.send(msg)

    @commands.command(hidden=False, aliases=['сервера'])
    async def servers(self, ctx):
        '''Отображает список текущих подключенных Серверов  (BOT OWNER ONLY)'''
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def leaveserver(self, ctx, guildid: str):
        '''Выход с сервера (BOT OWNER ONLY)

        Пример:
        -----------

        :leaveserver 102817255661772800
        '''
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.bot.get_guild(guildid)
            if guild:
                await guild.leave()
                msg = f':ok: Выход из {guild.name} успешен!'
            else:
                msg = ':x: Не удалось найти подходящую гильдию для этого идентификатора!'
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def echo(self, ctx, channel: str, *message: str):
        '''Выводит сообщение в качестве бота на определенном канале. Пример: ~echo id_канала 'сообщение' '''
        channel = self.bot.get_channel(int(channel))
        msg = ' '.join(message)
        await channel.send(msg)
        await ctx.message.delete()

    @commands.command(hidden=False)
    async def disc(self, ctx, disc: str):
        '''Возвращает пользователей с соответствующим кодом(под ником всегда). Пример: ~disc 0876'''

        discriminator = disc
        memberList = ''

        for guild in self.bot.guilds:
            for member in guild.members:
                if member.discriminator == discriminator and member.discriminator not in memberList:
                    memberList += f'{member}\n'

        if memberList:
            await ctx.send(memberList)
        else:
            await ctx.send(':x: Не смог найти никого')

    @commands.command(hidden=True)
    @commands.bot_has_permissions(manage_nicknames = False)
    async def nickname(self, ctx, *name):
        '''Изменение имени сервера от бота (BOT OWNER ONLY)'''
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f':ok: Измените мой ник сервера на: **{nickname}**'
        else:
            msg = f':ok: Сброс с моего сервера ник на: **{ctx.me.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.bot_has_permissions(manage_nicknames = False)
    async def setnickname(self, ctx, member: discord.Member=None, *name):
        '''Изменение псевдонима пользователя (BOT OWNER ONLY)'''
        if member == None:
            member = ctx.author
        nickname = ' '.join(name)
        await member.edit(nick=nickname)
        if nickname:
            msg = f':ok: Изменить ник из {member} в: **{nickname}**'
        else:
            msg = f':ok: Сбросить ник для {member} на: **{member.name}**'
        await ctx.send(msg)

    @commands.command(hidden=True)
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.channel)
    async def test(self, ctx):
        '''Test Test Test'''
        await ctx.send('Test')
        await self.bot.AppInfo.owner.send('Test')
        await ctx.send(self.bot.cogs)

def setup(bot):
    bot.add_cog(admin(bot))
