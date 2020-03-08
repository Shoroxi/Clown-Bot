import time
import os
import platform
import re
import asyncio
import inspect
import textwrap
from datetime import datetime, timedelta
from collections import Counter
import aiohttp
import discord
from discord.ext import commands
import loadconfig

class Plural:
    def __init__(self, **attr):
        iterator = attr.items()
        self.name, self.value = next(iter(iterator))

    def __str__(self):
        v = self.value
        if v > 1:
            return '%s %sn' % (v, self.name)
        return '%s %s' % (v, self.name)

    def __format__(self, format_spec):
        v = self.value
        singular, sep, plural = format_spec.partition('|')
        plural = plural or f'{singular}s'
        if abs(v) != 1:
            return f'{v} {plural}'
        return f'{v} {singular}'

class utility(commands.Cog):
    '''Общие / полезные команды, которые больше нигде не вписываются'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @staticmethod
    def _getRoles(roles):
        string = ''
        for role in roles[::-1]:
            if not role.is_default():
                string += f'{role.mention}, '
        if string == '':
            return 'None'
        else:
            return string[:-2]

    @staticmethod
    def _getEmojis(emojis):
        string = ''
        for emoji in emojis:
            string += str(emoji)
        if string == '':
            return 'None'
        else:
            return string[:1000] #The maximum allowed charcter amount for embed fields

    @commands.command(alieses=['статус'])
    async def status(self, ctx):
        '''Информация о боте'''
        timeUp = time.time() - self.bot.startTime
        hours = timeUp / 3600
        minutes = (timeUp / 60) % 60
        seconds = timeUp % 60

        admin = self.bot.AppInfo.owner
        users = 0
        channel = 0
        if len(self.bot.commands_used.items()):
            commandsChart = sorted(self.bot.commands_used.items(), key=lambda t: t[1], reverse=False)
            topCommand = commandsChart.pop()
            commandsInfo = '{} (Top-Command: {} x {})'.format(sum(self.bot.commands_used.values()), topCommand[1], topCommand[0])
        else:
            commandsInfo = str(sum(self.bot.commands_used.values()))
        for guild in self.bot.guilds:
            users += len(guild.members)
            channel += len(guild.channels)

        embed = discord.Embed(color=ctx.me.top_role.colour)
        embed.set_footer(text='Этот бот с открытым исходным кодом на GitHub:')
        embed.set_thumbnail(url=ctx.me.avatar_url)
        embed.add_field(name='Админ', value=admin, inline=False)
        embed.add_field(name='Время от запуска', value='{0:.0f} Часовой, {1:.0f} Минут {2:.0f} Секунды\n'.format(hours, minutes, seconds), inline=False)
        embed.add_field(name='Наблюдаемые Пользователи', value=users, inline=True)
        embed.add_field(name='Наблюдаемые Серверы', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='Наблюдаемый Канал', value=channel, inline=True)
        embed.add_field(name='Выполняемые Команды', value=commandsInfo, inline=True)
        embed.add_field(name='Версия бота', value=self.bot.botVersion, inline=True)
        embed.add_field(name='Версия дискорд.py', value=discord.__version__, inline=True)
        embed.add_field(name='Версия питона', value=platform.python_version(), inline=True)
        # embed.add_field(name='Speicher Auslastung', value=f'{round(memory_usage(-1)[0], 3)} MB', inline=True)
        embed.add_field(name='Операционная система', value=f'{platform.system()} {platform.release()} {platform.version()}', inline=False)
        await ctx.send('**:information_source:** Информация об этом боте:', embed=embed)

    # @commands.command()
    # @commands.cooldown(1, 2, commands.cooldowns.BucketType.guild)
    # async def github(self, ctx):
    #     '''In progress'''
    #     url = 'https://api.github.com/repos/Der-Eddy/discord_bot/stats/commit_activity'
    #     async with aiohttp.get(url) as r:
    #         if r.status == 200:
    #             content = await r.json()
    #             commitCount = 0
    #             for week in content:
    #                 commitCount += week['total']
    #
    #             embed = discord.Embed(title='GitHub Repo Stats', type='rich', color=0xf1c40f) #Golden
    #             embed.set_thumbnail(url='https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png')
    #             embed.add_field(name='Commits', value=commitCount, inline=True)
    #             embed.add_field(name='Link', value='https://github.com/Der-Eddy/discord_bot')
    #             await ctx.send(embed=embed)
    #         else:
    #             await ctx.send(':x: Konnte nicht aufs GitHub API zugreifen\nhttps://github.com/Der-Eddy/discord_bot')

    #@commands.command(aliases=['info'])
    #async def about(self, ctx):
    #    '''Информация'''
    #    msg = ''
    #    msg += '\n\n'
    #    msg += ''

    #    embed = discord.Embed(color=ctx.me.top_role.colour)
    #    embed.set_footer(text='Этот Бот также бесплатный, с открытым исходным кодом,с помощью Python и discord.py! \n')
    #    embed.set_thumbnail(url=ctx.me.avatar_url)
    #    embed.add_field(name='**:information_source: Shinobu Oshino **', value=msg, inline=False)
    #    await ctx.send(embed=embed)

    @commands.command(aliases=['архив'])
    @commands.cooldown(1, 60, commands.cooldowns.BucketType.channel)
    async def log(self, ctx, *limit: int):
        '''Архивирует журнал текущего канала и загружает его как вложение

        Пример:
        -----------

        ~log 100
        '''
        if not limit:
            limit = 10
        else:
            limit = limit[0]
        logFile = f'{ctx.channel}.log'
        counter = 0
        with open(logFile, 'w', encoding='UTF-8') as f:
            f.write(f'Архивированные сообщения с канала: {ctx.channel} am {ctx.message.created_at.strftime("%d.%m.%Y %H:%M:%S")}\n')
            async for message in ctx.channel.history(limit=limit, before=ctx.message):
                try:
                    attachment = '[Вложенный Файл: {}]'.format(message.attachments[0].url)
                except IndexError:
                    attachment = ''
                f.write('{} {!s:20s}: {} {}\r\n'.format(message.created_at.strftime('%d.%m.%Y %H:%M:%S'), message.author, message.clean_content, attachment))
                counter += 1
        msg = f':ok: {counter} Сообщения были заархивированы!'
        f = discord.File(logFile)
        await ctx.send(file=f, content=msg)
        os.remove(logFile)

    @log.error
    async def log_error(self, error, ctx):
        if isinstance(error, commands.errors.CommandOnCooldown):
            seconds = str(error)[34:]
            await ctx.send(f':alarm_clock: Cooldown! Попробуйте через {seconds} позже')

    @commands.command(aliases=['инвайт'])
    async def invite(self, ctx):
        '''Создает ссылку Invite для текущего канала'''
        
        invite = await ctx.channel.create_invite(max_uses=0, unique=True)
        msg = f'Invite ссылка для **#{ctx.channel.name}** на сервер **{ctx.guild.name}**:\n{invite.url}'
        await ctx.author.send(msg)

    @commands.command(alises=['профиль'])
    async def profile(self, ctx, member: discord.Member=None):
        '''Выводит информацию о пользователе

        Пример:
        -----------

        ~whois @Der-Eddy#6508
        '''
        if member == None:
            member = ctx.author

        if member.top_role.is_default():
            topRole = 'everyone' #to prevent @everyone spam
            topRoleColour = '#000000'
        else:
            topRole = member.top_role
            topRoleColour = member.top_role.colour

        if member is not None:
            embed = discord.Embed(title=member.name)
            embed = discord.Embed(color=member.top_role.colour)
            embed.set_footer(text=f'UserID: {member.id}')
            embed.set_thumbnail(url=member.avatar_url)
            if member.name != member.display_name:
                fullName = f'{member} ({member.display_name})'
            else:
                fullName = member
            embed.add_field(name=member.name, value=fullName, inline=False)
            embed.add_field(name='Присоединился к Discord', value='{}\n(Дней с тех пор: {})'.format(member.created_at.strftime('%d.%m.%Y'), (datetime.now()-member.created_at).days), inline=True)
            embed.add_field(name='Присоединился к Серверу', value='{}\n(Дней с тех пор: {})'.format(member.joined_at.strftime('%d.%m.%Y'), (datetime.now()-member.joined_at).days), inline=True)
            embed.add_field(name='Аватар-Ссылка', value=member.avatar_url, inline=False)
            embed.add_field(name='Роли', value=self._getRoles(member.roles), inline=True)
            embed.add_field(name='Цвет роли', value='{} ({})'.format(topRoleColour, topRole), inline=True)
            embed.add_field(name='Статус', value=member.status, inline=True)
            await ctx.send(embed=embed)
        else:
            msg = ':no_entry:Вы не указали пользователя!'
            await ctx.send(msg)

#    @commands.command(aliases=['e'])
#    async def emoji(self, ctx, emojiname: str):
#        '''Возвращает увеличенную версию указанного Emojis
#
#        Пример:
#        -----------

#        ~emoji Emilia
#        '''
#        emoji = discord.utils.find(lambda e: e.name.lower() == emojiname.lower(), self.bot.emojis)
#        if emoji:
#            tempEmojiFile = 'tempEmoji.png'
#            async with aiohttp.ClientSession() as cs:
#                async with cs.get(emoji.url) as img:
#                    with open(tempEmojiFile, 'wb') as f:
#                        f.write(await img.read())
#                f = discord.File(tempEmojiFile)
#                await ctx.send(file=f)
#                os.remove(tempEmojiFile)
#        else:
#            await ctx.send(':x: К сожалению, не удалось найти указанный Emoji :(')

    @commands.command(aliases=['эмоции'])
    async def emojis(self, ctx):
        '''Выводит все Emojis, к которым бот имеет доступ'''
        msg = ''
        for emoji in self.bot.emojis:
            if len(msg) + len(str(emoji)) > 1000:
                await ctx.send(msg)
                msg = ''
            msg += str(emoji)
        await ctx.send(msg)

    @commands.command(pass_context=True)
    async def server(self, ctx):
        '''Выводит сведения о действующей гильдии'''
        emojis = self._getEmojis(ctx.guild.emojis)
        #print(emojis)
        roles = self._getRoles(ctx.guild.roles)
        embed = discord.Embed(color=0xf1c40f) #Golden
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='Имя', value=ctx.guild.name, inline=True)
        embed.add_field(name='ID', value=ctx.guild.id, inline=True)
        embed.add_field(name='Владелец', value=ctx.guild.owner, inline=True)
        embed.add_field(name='Регион', value=ctx.guild.region, inline=True)
        embed.add_field(name='Члены', value=ctx.guild.member_count, inline=True)
        embed.add_field(name='Создан на', value=ctx.guild.created_at.strftime('%d.%m.%Y'), inline=True)
        if ctx.guild.system_channel:
            embed.add_field(name='Стандартный Канал', value=f'#{ctx.guild.system_channel}', inline=True)
        embed.add_field(name='АФК таймер', value=f'{int(ctx.guild.afk_timeout / 60)} min', inline=True)
        embed.add_field(name='Участники', value=ctx.guild.shard_id, inline=True)
        embed.add_field(name='Роли', value=roles, inline=True)
        embed.add_field(name='Эмоджи', value=emojis, inline=True)
        await ctx.send(embed=embed)

    #Shameful copied from https://github.com/Rapptz/RoboDanny/blob/b513a32dfbd4fdbd910f7f56d88d1d012ab44826/cogs/meta.py

    #Stolen from https://github.com/Rapptz/RoboDanny/blob/b513a32dfbd4fdbd910f7f56d88d1d012ab44826/cogs/meta.py
    #@commands.command(hidden=True)
    #async def source(self, ctx, *, command: str = None):
    #    '''Отображает исходный код для команды на GitHub

    #    Пример:
    #    -----------

    #    :source kawaii
    #    '''
    #    source_url = 'https://github.com/Der-Eddy/discord_bot'
    #    if command is None:
    #        await ctx.send(source_url)
    #        return

    #    obj = self.bot.get_command(command.replace('.', ' '))
    #    if obj is None:
    #        return await ctx.send(':x: Не удалось найти команду')

        # since we found the command we're looking for, presumably anyway, let's
        # try to access the code itself
    #    src = obj.callback.__code__
    #    lines, firstlineno = inspect.getsourcelines(src)
    #    sourcecode = inspect.getsource(src).replace('```', '')
    #    if not obj.callback.__module__.startswith('discord'):
            # not a built-in command
    #        location = os.path.relpath(src.co_filename).replace('\\', '/')
    #    else:
    #        location = obj.callback.__module__.replace('.', '/') + '.py'
    #        source_url = 'https://github.com/Rapptz/discord.py'

    #    if len(sourcecode) > 1900:
    #        final_url = '{}/blob/master/{}#L{}-L{}'.format(source_url, location, firstlineno, firstlineno + len(lines) - 1)
    #    else:
    #        final_url = '<{}/blob/master/{}#L{}-L{}>\n```Python\n{}```'.format(source_url, location, firstlineno, firstlineno + len(lines) - 1, sourcecode)

    #    await ctx.send(final_url)

    @commands.command(hidden=True)
    async def roleUsers(self, ctx, *roleName: str):
        '''Список всех пользователей роли'''
        codingLoungeID= 589528167354597376
        if ctx.guild.id in [codingLoungeID]:
            codingRankList = ['Бармен', 'Половой партнер', 'Server Booster', 'Подпизжиг', 'Дамма сервера', 'Заядлый алкаш', 'R6S', 'OverDroch', 'CS:ФУ', 'LigaLegend', 'DOTA', 'MineСруфт', 'Terraria', 'WOT', 'Apex', 'Андроид ебаный', 'Живой', 'Бизнесмен', '3D,шнэг', 'Хуцкер', 'AnimeGURU', 'Droch', '@everyone']
            roleName = []
            roleName.append(['дамма сервера', 'Дамма сервера'])
            roleName.append(['r6s', 'R6S' ])
            roleName.append(['overdroch', 'OverDroch'])
            roleName.append(['cs:фу', 'CS:ФУ' ])
            roleName.append(['ligalegend', 'LigaLegend'])
            roleName.append(['dota', 'DOTA'])
            roleName.append(['mineсруфт', 'MineСруфт'])
            roleName.append(['terraria', 'Terraria'])
            roleName.append(['wot', 'WOT'])
            roleName.append(['apex', 'Apex'])
            roleName.append(['живой', 'Живой' ])
            roleName.append(['андроид ебаный', 'Андроид ебаный'])
            roleName.append(['бизнесмен', 'Бизнесмен'])
            roleName.append(['3d,шнэг', '3D,шнэг'])
            roleName.append(['хуцкер', 'Хуцкер' ])
            roleName.append(['animeguru', 'AnimeGURU'])
            roleName.append(['droch', 'Droch'])

            try:
                rankName = roleName[' '.join(rankName).lower()]
            except KeyError:
                rankName = ' '.join(rankName)

            if not rankName in codingRankList:
                await ctx.send(':x: Не смог найти эту роль! '+ str(rankName) +' Используйте `~rank`, чтобы перечислить все доступные ранги')
                return
            

            #if msg == '':
            #    await ctx.send(':x: Не удалось найти пользователя с этой ролью! ' + str(role))
            #else:
            #    await ctx.send(msg)

    @commands.command(hidden=True)
    async def games(self, ctx, *scope):
        '''Показывает, какие игры, как часто играют на сервере. Пример: '''
        games = Counter()
        for member in ctx.guild.members:
            if member.game != None:
                games[member.game] += 1
        msg = ':chart: Игры, которые в настоящее время играют на этом сервере\n'
        msg += '```js\n'
        msg += '{!s:40s}: {!s:>3s}\n'.format('Имя', 'Количество')
        chart = sorted(games.items(), key=lambda t: t[1], reverse=True)
        for index, (name, amount) in enumerate(chart):
            if len(msg) < 1950:
                msg += '{!s:40s}: {!s:>3s}\n'.format(name, amount)
            else:
                amount = len(chart) - index
                msg += f'+ {amount} другой'
                break
        msg += '```'
        await ctx.send(msg)

    @commands.command(aliases=['ранг', 'роль', 'роли'])
    async def role(self, ctx, *rankName: str):
        '''Перечисление всех рангов или присоединение к определенному рангу

        Пример:
        -----------
        ~role
        ~role R6S
        '''
        codingLoungeID = 589528167354597376
        
        codingRankList = ['R6S', 'OverDroch', 'CS:ФУ', 'LigaLegend', 'DOTA', 'MineСруфт', 'Terraria', 'WOT', 'Apex', 'Живой', 'Бизнесмен', '3D,шнэг', 'Хуцкер', 'AnimeGURU', 'Droch']
        if ctx.guild.id == codingLoungeID:
            rankList = codingRankList

        if len(rankName) == 0 and ctx.guild.id not in [codingLoungeID] or ''.join(rankName) == 'all':
            rolesList = '`'
            for roleServer in ctx.guild.roles:
                if not roleServer.is_default():
                    count = 0
                    for member in ctx.guild.members:
                        if roleServer in member.roles:
                            count += 1
                    rolesList += f'{roleServer.name:30}{count} Members\n'
            embed = discord.Embed(color=0xf1c40f) #Golden
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='Ranks', value=rolesList + '`', inline=True)
            await ctx.send(embed=embed)
        elif len(rankName) == 0 and ctx.guild.id in [codingLoungeID]:
            rolesList = '`'
            for role in rankList:
                count = 0
                roleServer = discord.utils.get(ctx.guild.roles, name=role)
                for member in ctx.guild.members:
                    if roleServer in member.roles:
                        count += 1
                rolesList += f'{role:20}{count} Members\n'
            embed = discord.Embed(color=0x3498db) #Blue
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text='Используйте "~role RANKNAME" чтобы добавить роль')
            embed.add_field(name='Роли', value=rolesList + '`', inline=True)
            await ctx.send(embed=embed)
        elif ctx.guild.id not in [codingLoungeID]:
            await ctx.send(':x: Эта команда работает только на сервере Gay Bar: Reborn!')
        elif ctx.guild.id in [codingLoungeID]:
            synonyms = []
            synonyms.append(['дамма сервера', 'Дамма сервера'])
            synonyms.append(['r6s', 'R6S' ])
            synonyms.append(['overdroch', 'OverDroch'])
            synonyms.append(['cs:фу', 'CS:ФУ' ])
            synonyms.append(['ligalegend', 'LigaLegend'])
            synonyms.append(['dota', 'DOTA'])
            synonyms.append(['mineсруфт', 'MineСруфт'])
            synonyms.append(['terraria', 'Terraria'])
            synonyms.append(['wot', 'WOT'])
            synonyms.append(['apex', 'Apex'])
            synonyms.append(['живой', 'Живой' ])
            synonyms.append(['андроид ебаный', 'Андроид ебаный'])
            synonyms.append(['бизнесмен', 'Бизнесмен'])
            synonyms.append(['3d,шнэг', '3D,шнэг'])
            synonyms.append(['хуцкер', 'Хуцкер' ])
            synonyms.append(['animeguru', 'AnimeGURU'])
            synonyms.append(['droch', 'Droch'])


            synonyms_dict = dict(synonyms)

            try:
                rankName = synonyms_dict[' '.join(rankName).lower()]
            except KeyError:
                rankName = ' '.join(rankName)

            if not rankName in rankList:
                await ctx.send(':x: Не смог найти эту роль! '+ str(rankName) +' Используйте `~role`, чтобы перечислить все доступные ранги')
                return

            rank = discord.utils.get(ctx.guild.roles, name=rankName)
            if rank in ctx.message.author.roles:
                try:
                    await ctx.author.remove_roles(rank)
                except:
                    pass
                await ctx.send(f':negative_squared_cross_mark: Роль **{rank}** убрана у **{ctx.author.mention}**')
            else:
                try:
                    await ctx.author.add_roles(rank)
                except:
                    pass
                await ctx.send(f':white_check_mark: Роль **{rank}** добавлена к **{ctx.author.mention}**')

    @commands.command(aliases=['vote', 'голосование', 'опрос'])
    async def addvote(self, ctx, votecount = 'bool'):
        '''Добавляет эмоции в качестве реакций для голосования/опросов'''
        if votecount.lower() == 'bool':
            emote_list = ['✅', '❌']
        elif votecount in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            #emotes = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            #for whatever reason, the above won't work
            emotes = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']
            emote_list = []
            for i in range (0, int(votecount)):
                emote_list.append(emotes[i])
        else:
            await ctx.send(':x: Пожалуйста, укажите число от 1 до 10')

        message = await ctx.channel.history(limit=1, before=ctx.message).flatten()
        try:
            await ctx.message.delete()
        except:
            pass

        for emote in emote_list:
            await message[0].add_reaction(emote)

    # This command needs to be at the end due to it's name
    @commands.command()
    async def commands(self, ctx):
        '''Показывает, сколько раз команда использовалась с момента последнего запуска'''
        msg = ':chart: Список выполняемых команд (с момента последнего запуска)\n'
        msg += 'В общей сложности: {}\n'.format(sum(self.bot.commands_used.values()))
        msg += '```js\n'
        msg += '{!s:15s}: {!s:>4s}\n'.format('Имя', 'Количество')
        chart = sorted(self.bot.commands_used.items(), key=lambda t: t[1], reverse=True)
        for name, amount in chart:
            msg += '{!s:15s}: {!s:>4s}\n'.format(name, amount)
        msg += '```'
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(utility(bot))
