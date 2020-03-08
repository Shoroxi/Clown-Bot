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
        await ctx.send('**:ok:** DING DING DING')

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

    @commands.command(hidden=False,aliases=['тэг'])
    async def tags(self, ctx, command: str, *arg):
        '''Создает или выводит теги
        Пример:
        -----------
        ~tags COMMAND
            Выводит случайное изображение под командой
        ~tags add COMMAND BILDURL
            Добавляет изображение в команду
        ~tags del ID
            Удаляет запись с соответствующим идентификатором, только для Модараторов и создателей записи
        ~tags list
            Указывает полный список команд и соответствующих ссылок
        '''
        with sqlite3.connect(self.db) as con:
            c = con.cursor()
            if command == 'add' or command == 'new':
                if len(arg) > 1:
                    command = arg[0].lower()
                    content = list(arg[1:])
                    c.execute('INSERT INTO "reactions" ("command","url","author") VALUES (?, ?, ?)', (command, ' '.join(content), str(ctx.message.author)))
                    con.commit()
                    await ctx.send(':ok: Tag **{}** hinzugefügt!'.format(arg[0].lower()))
            elif command == 'del' or command == 'rm':
                if await ctx.bot.is_owner(ctx.author):
                    c.execute('DELETE FROM "reactions" WHERE "id" in (?)', (int(arg[0]), ))
                else:
                    c.execute('DELETE FROM "reactions" WHERE "id" in (?) AND "author" IN (?)', (int(arg[0]), str(ctx.message.author)))
                con.commit()
                await ctx.send(':put_litter_in_its_place: Tag-ID #{} gelöscht!'.format(arg[0].lower()))
            elif command == 'list':
                lst = c.execute('SELECT * FROM "reactions"')
                msg = ''
                for i in lst:
                    msg += '**ID:** {:>3} | **Command:** {:>15} | **Author:** {}\n'.format(i[0], i[1], i[3])
                await ctx.send(msg)
            else:
                lst = c.execute('SELECT * FROM "reactions" WHERE "command" LIKE (?)', (command,))
                reaction = random.choice(lst.fetchall())
                await ctx.send(reaction[2])
            c.close()

    @commands.command(hidden=True,aliases=['joke'])
    async def pun(self, ctx):
        '''Смешинки'''
        puns = ['Что говорит одна спичка о другой спичке?\n Давай, давай прорвемся',
                'Сколько немцев нужно, чтобы сменить лампочку?\n Во - первых, мы без юмора и эффективно.',
                'Где живет кошка?\n В Меже.',
                'Wie begrüßen sich zwei plastische Chirurgen?\n "Was machst du denn heute für ein Gesicht?"',
                'Warum essen Veganer kein Huhn?\n Könnte Ei enthalten',
                '85% der Frauen finden ihren Arsch zu dick, 10% zu dünn, 5% finden ihn so ok, wie er ist und sind froh, dass sie ihn geheiratet haben...',
                'Meine Freundin meint, ich wär neugierig...\n...zumindest\' steht das in ihrem Tagebuch.',
                '"Schatz, Ich muss mein T-Shirt waschen! Welches Waschmaschinen Programm soll ich nehmen?" - "Was steht denn auf dem T-Shirt drauf?"\n "Slayer!"',
                'Gestern erzählte ich meinem Freund, dass ich schon immer dieses Ding aus Harry Potter reiten wollte.\n"einen Besen?" "nein, Hermine."',
                'Warum gehen Ameisen nicht in die Kirche?\nSie sind in Sekten.',
                'Was steht auf dem Grabstein eines Mathematikers?\n"Damit hat er nicht gerechnet."',
                'Wenn ein Yogalehrer seine Beine senkrecht nach oben streckt und dabei furzt, welche Yoga Figur stellt er da?\n Eine Duftkerze',
                'Warum ging der Luftballon kaputt?\n Aus Platzgründen.',
                'Ich wollte Spiderman anrufen, aber er hatte kein Netz.',
                'Was vermisst eine Schraube am meisten? Einen Vater',
                'Geht ein Panda über die Straße. Bam....Bus!']
        emojis = [':laughing:', ':smile:', ':joy:', ':sob:', ':rofl:']
        msg = f'{random.choice(emojis)} {random.choice(puns)}'
        await ctx.send(msg)

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
