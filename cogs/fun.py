import random
import urllib.parse
import sqlite3
import asyncio
import aiohttp
import discord
import io
import re
import urllib
from discord.ext import commands
import loadconfig

class fun(commands.Cog):
    db = 'reaction.db'

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @commands.command(aliases=['жаба', 'nodejs', 'js'], qualified_name="жаба", description="Потому Что Java != Javscript")
    async def java(self, ctx):
        await ctx.send(':interrobang: Вы имели в виду jQuery, Javascript или Node.js? https://abload.de/img/2016-05-102130191kzpu.png')

    @commands.command(aliases=['%гея']) #пинг
    async def howgay(self,ctx):
        gay = ['100%! да ты бомба', '99% -_-.. а где уй в жопе?', '93%', '91%',  '89%',  '87%',  '85%',  '83%','81%', '79%', '77%', '75%', '73%', '71%', '69%', '67%', '65%', '63%', '60%', '59%', '57%',  '55%',  '53%', '51%', '50% истинный баланс', '49% а дотянуть не мог а?', '48%а дотянуть не мог а?', '47%', '45%', '43%', '42%', '40%', '38%', '36%', '34%', '32%',  '30%', '28%',  '26%',  '24%', '22%',  '20%',  '18%',  '16%',  '14%',  '12%',  '10%', '9% ты на грани', '8% ты на грани', '7% ты на грани', '6% ты на грани', '5% ты на грани', '4% ты на грани', '3% ты на грани', '2% ты на грани', '1% ты на грани', '0% кажется тебе здесь не место']
        await ctx.send(random.choice(gay))

    @commands.command(aliases=['ку', 'привет'])
    async def hello(self, ctx):
        '''Поздаровайся'''
        gifs = ['https://cdn.discordapp.com/attachments/102817255661772800/219512763607678976/large_1.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219512898563735552/large.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518948251664384/WgQWD.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518717426532352/tumblr_lnttzfSUM41qgcvsy.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519191290478592/tumblr_mf76erIF6s1qj96p1o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519729604231168/giphy_3.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519737971867649/63953d32c650703cded875ac601e765778ce90d0_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219519738781368321/17201a4342e901e5f1bc2a03ad487219c0434c22_hq.gif']
        msg = random.choice(gifs)
        embed = discord.Embed(title=':wave:')
        embed.set_image(url=msg)
        await ctx.send(embed=embed)
  
    #@commands.command()
    #async def gif(self, ctx, *keywords):
    #    """Retrieve the first search result from Giphy."""
    #    if keywords:
    #        keywords = "+".join(keywords)
    #    else:
    #        await ctx.send_help()
    #        return

    #    giphy_api_key = (await ctx.bot.get_shared_api_tokens("GIPHY")).get("api_key")
    #    if not giphy_api_key:
    #        await ctx.send(
    #            _("An API key has not been set! Please set one with `{prefix}giphycreds`.").format(
    #                prefix=ctx.clean_prefix
    #            )
    #        )
    #        return

    #    url = "http://api.giphy.com/v1/gifs/search?&api_key={}&q={}".format(
    #        giphy_api_key, keywords
    #    )

    #    async with self.session.get(url) as r:
    #        result = await r.json()
    #        if r.status == 200:
    #            if result["data"]:
    #                await ctx.send(result["data"][0]["url"])
    #            else:
    #                await ctx.send("No results found.")
    #        else:
    #            await ctx.send("Error contacting the Giphy API.")


    @commands.command(hidden=True, aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Прокунсультироваться с 8ball """
        ballresponse = [
        'да', 'нет', 'ты далбеб', 'хуй соси', 'Увы, да', 'Ответ отрицательный', 'А ведь и я раньше задавался этим вопросом', 'я чо ябу?', 'ХЗ', 'Как хачешь'
        ]
        answer = random.choice(ballresponse)
        await ctx.send(f"🎱 **Вопрос:** {question}\n**Ответ:** {answer}")
    
    @commands.command(aliases=['c++', 'c#', 'objective-c'])
    async def csharp(self, ctx):
        '''Как вы вообще должны смотреть???'''
        await ctx.send(':interrobang: Вы имели в виду C, C++, C# или Objective-C? https://i.imgur.com/Nd4aAXO.png')

    @commands.command()
    async def praise(self, ctx):
        '''Слава солнцу'''
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')

    @commands.command()
    async def css(self, ctx):
        '''Counter Strike: Source'''
        await ctx.send('http://i.imgur.com/TgPKFTz.gif')

    @commands.command(alieses=['смерть'])
    async def countdown(self, ctx):
        '''Это последний отсчет времени.'''
        countdown = ['five', 'four', 'three', 'two', 'one']
        for num in countdown:
            await ctx.send('**:{0}:**'.format(num))
            await asyncio.sleep(1)
        await ctx.send('**:ok:** НАЕБАЛ')

    @commands.command(aliases=['ранд'])
    async def random(self, ctx, *arg):
        '''Выводит случайное число или победителя

        Пример:
        -----------
        ~random
        ~random coin
        ~random 6
        ~random 10 20
        ~random @Он
        ~random choice @Я @он @мы
        '''
        if ctx.invoked_subcommand is None:
            if not arg:
                start = 1
                end = 100
            elif arg[0] == 'flip' or arg[0] == 'coin':
                coin = ['Орел', 'Решка']
                await ctx.send(f':arrows_counterclockwise: {random.choice(coin)}')
                return
            elif arg[0] == 'choice':
                choices = list(arg)
                choices.pop(0)
                await ctx.send(f':congratulations: Победитель: {random.choice(choices)}')
                return
            elif arg[0] == 'user':
                online = self.userOnline(ctx.guild.members)
                randomuser = random.choice(online)
                if ctx.channel.permissions_for(ctx.author).mention_everyone:
                    user = randomuser.mention
                else:
                    user = randomuser.display_name
                await ctx.send(f':congratulations: Победитель {user}')
                return
            elif len(arg) == 1:
                start = 1
                end = int(arg[0])
            elif len(arg) == 2:
                start = int(arg[0])
                end = int(arg[1])
            await ctx.send(f'**:arrows_counterclockwise:** Рандомное число: ({start} - {end}): {random.randint(start, end)}')

    @commands.command(aliases=['килл', 'убить'])
    async def kill(self, ctx, member:str):
        '''Python'''
        await ctx.send(f'R.I.P. {member}\nhttps://media.giphy.com/media/l41lGAcThnMc29u2Q/giphy.gif')

    @commands.command(aliases=['хайп'])
    async def hype(self, ctx):
        '''HYPE Поровозик CHOO CHOO'''
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.send(msg)

    @commands.command()
    async def xkcd(self, ctx,  *searchterm: str):
        '''Показывает последний или случайный xkcd комикс

        Пример:
        -----------
        ~xkcd
        ~xkcd r (random)
        '''
        apiUrl = 'https://xkcd.com{}info.0.json'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(apiUrl.format('/')) as r:
                js = await r.json()
                if ''.join(searchterm) == 'r':
                    randomComic = random.randint(0, js['num'])
                    async with cs.get(apiUrl.format('/' + str(randomComic) + '/')) as r:
                        if r.status == 200:
                            js = await r.json()
                comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
                date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
                msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(js['safe_title'], js['img'], js['alt'], comicUrl, date)
                await ctx.send(msg)

    #    @commands.command(hidden=False,aliases=['тэг'])
    #    async def tags(self, ctx, command: str, *arg):
    #        '''Создает или выводит теги
    #        Пример:
    #        -----------
    #        ~tags COMMAND
    #            Выводит случайное изображение под командой
    #        ~tags add COMMAND BILDURL
    #            Добавляет изображение в команду
    #        ~tags del ID
    #            Удаляет запись с соответствующим идентификатором, только для Модараторов и создателей записи
    #        ~tags list
    #            Указывает полный список команд и соответствующих ссылок
    #        '''
    #        with sqlite3.connect(self.db) as con:
    #            c = con.cursor()
    #            if command == 'add' or command == 'new':
    #                if len(arg) > 1:
    #                    command = arg[0].lower()
    #                    content = list(arg[1:])
    #                    c.execute('INSERT INTO "reactions" ("command","url","author") VALUES (?, ?, ?)', (command, ' '.join(content), str(ctx.message.author)))
    #                    con.commit()
    #                    await ctx.send(':ok: Tag **{}** hinzugefügt!'.format(arg[0].lower()))
    #            elif command == 'del' or command == 'rm':
    #                if await ctx.bot.is_owner(ctx.author):
    #                    c.execute('DELETE FROM "reactions" WHERE "id" in (?)', (int(arg[0]), ))
    #                else:
    #                    c.execute('DELETE FROM "reactions" WHERE "id" in (?) AND "author" IN (?)', (int(arg[0]), str(ctx.message.author)))
    #                con.commit()
    #                await ctx.send(':put_litter_in_its_place: Tag-ID #{} gelöscht!'.format(arg[0].lower()))
    #            elif command == 'list':
    #                lst = c.execute('SELECT * FROM "reactions"')
    #                msg = ''
    #                for i in lst:
    #                    msg += '**ID:** {:>3} | **Command:** {:>15} | **Author:** {}\n'.format(i[0], i[1], i[3])
    #                await ctx.send(msg)
    #            else:
    #                lst = c.execute('SELECT * FROM "reactions" WHERE "command" LIKE (?)', (command,))
    #                reaction = random.choice(lst.fetchall())
    #                await ctx.send(reaction[2])
    #            c.close()

    @commands.command(aliases=['кот'])
    async def cat(self,ctx):
        """Рандомный кота"""
        async with aiohttp.ClientSession() as session:
            async with session.get('http://aws.random.cat/meow') as r:
            # 200 -> everything fine.
                if r.status == 200:
                    content = await r.json()
                    vid=content['file'].replace('\ ', ' ')
                    embed = discord.Embed(title='Держи котейку')
                    embed.set_image(url=vid)
                    await ctx.send(embed=embed)
            await session.close()
 
    @commands.command(aliases=['собака'])
    async def dog(self,ctx):
            """Рандомный собаку"""
            # changes to aiohttp -> set the session to a var and call things with it. Kill the session when done...
            async with aiohttp.ClientSession() as session:
                async with session.get("https://random.dog/woof") as r:
                    if r.status == 200:
                        dog_link = await r.text()
                        vid="https://random.dog/" + dog_link
                        embed = discord.Embed(title='Держи собачку')
                        embed.set_image(url=vid)
                        await ctx.send(embed=embed)
            await session.close()
    

def setup(bot):
    bot.add_cog(fun(bot))
