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

    @commands.command(aliases=['clr'])
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def clear(self, ctx, *limit):
        '''Удаление нескольких сообщений сразу (MOD ONLY)
        Пример:
        -----------
        :purge 100
        '''
        try:
            limit = int(limit[0])
        except IndexError:
            limit = 1
        deleted = 0
        while limit >= 1:
            cap = min(limit, 100)
            deleted += len(await ctx.channel.purge(limit=cap, before=ctx.message))
            limit -= cap
        tmp = await ctx.send(f'**:put_litter_in_its_place:** {deleted} Сообщения удалены')
        await asyncio.sleep(15)
        await tmp.delete()
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member = None, *reason):
        '''Пинает член с обоснованием (MOD ONLY)

        Пример:
        -----------

        :kick @Der-Eddy#6508
        '''
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.kick(reason=reason)
        else:
            await ctx.send('**:no_entry:** Пользователь не указан!')

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member=None, *reason):
        '''Запрещает члену с обоснованием (MOD ONLY)

        Пример:
        -----------

        :ban @Der-Eddy#6508
        '''
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.ban(reason=reason)
        else:
            await ctx.send('**:no_entry:** Пользователь не указан!')

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def unban(self, ctx, user: int=None, *reason):
        '''Лишает члена с обоснованием (MOD ONLY)
        Необходимо указать идентификатор пользователя, Имя + Discriminator недостаточно

        Пример:
        -----------

        :unban 102815825781596160
        '''
        user = discord.User(id=user)
        if user is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await ctx.guild.unban(user, reason=reason)
        else:
            await ctx.send('**:no_entry:** Пользователь не указан!')

    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def bans(self, ctx):
        '''Список зарегистрированных пользователей (MOD ONLY)'''
        users = await ctx.guild.bans()
        if len(users) > 0:
            msg = f'`{"ID":21}{"Name":25} Begründung\n'
            for entry in users:
                userID = entry.user.id
                userName = str(entry.user)
                if entry.user.bot:
                    username = '🤖' + userName #:robot: emoji
                reason = str(entry.reason) #Could be None
                msg += f'{userID:<21}{userName:25} {reason}\n'
            embed = discord.Embed(color=0xe74c3c) #Red
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f'Server: {ctx.guild.name}')
            embed.add_field(name='Ranks', value=msg + '`', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('**:negative_squared_cross_mark:** Нет запрещенных пользователей!')

    @commands.command(alias=['clearreactions'])
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def removereactions(self, ctx, messageid : str):
        '''Удаляет все Emoji Reactions из сообщения (MOD ONLY)

        Пример:
        -----------

        :removereactions 247386709505867776
        '''
        message = await ctx.channel.get_message(messageid)
        if message:
            await message.clear_reactions()
        else:
            await ctx.send('**:x:** Не удалось найти сообщение с этим идентификатором!')

    @commands.command()
    async def permissions(self, ctx):
        '''Список всех прав бота'''
        permissions = ctx.channel.permissions_for(ctx.me)

        embed = discord.Embed(title=':customs:  Permissions', color=0x3498db) #Blue
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Channel', value=ctx.channel, inline=False)

        for item, valueBool in permissions:
            if valueBool == True:
                value = ':white_check_mark:'
            else:
                value = ':x:'
            embed.add_field(name=item, value=value)

        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def hierarchy(self, ctx):
        '''Список иерархии ролей текущего сервера'''
        msg = f'Иерархия ролей для серверов **{ctx.guild}**:\n\n'
        roleDict = {}

        for role in ctx.guild.roles:
            if role.is_default():
                roleDict[role.position] = 'everyone'
            else:
                roleDict[role.position] = role.name

        for role in sorted(roleDict.items(), reverse=True):
            msg += role[1] + '\n'
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(mod(bot))
