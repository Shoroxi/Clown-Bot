import sys
import random
import re
import asyncio
import aiohttp
import discord
from discord.ext import commands
import xml.etree.ElementTree as ET
import loadconfig
import io
import os
class anime(commands.Cog):
    '''Все вокруг Anime'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    def checkRole(self, user, roleRec):
        ok = False
        for all in list(user.roles):
            if all.name == roleRec:
                ok = True
        return ok

    @commands.command(hidden=True)
    async def kawaii(self, ctx):
        '''Выводит случайное изображение kawaii'''
        print(loadconfig.__kawaiichannel__)
        if loadconfig.__kawaiichannel__:
            pins = await self.bot.get_channel(loadconfig.__kawaiichannel__).pins()
            rnd = random.choice(pins)
            img = rnd.attachments[0].url
            emojis = [':blush:', ':flushed:', ':heart_eyes:', ':heart_eyes_cat:', ':heart:']
            await ctx.send(f'{random.choice(emojis)} В: {rnd.author.display_name}: {img}')
        else:
            await ctx.send('**:no_entry:** Канал для бота не был установлен! Пожалуйста, свяжитесь с администратором бота')

    @commands.command()
    async def nep(self, ctx):
        '''NEP'''
        neps = ['https://cdn.discordapp.com/attachments/102817255661772800/219530759881359360/community_image_1421846157.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535598187184128/tumblr_nv25gtvX911ubsb68o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535698309545984/tumblr_mpub9tTuZl1rvrw2eo2_r1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535820430770176/dd9f3cc873f3e13fe098429388fc24242a545a21_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535828773371904/tumblr_nl62nrrPar1u0bcbmo1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535828995538944/dUBNqIH.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219535906942615553/b3886374588ec93849e1210449c4561fa699ff0d_hq.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536353841381376/tumblr_nl9wb2qMFD1u3qei8o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536345176080384/tumblr_njhahjh1DB1t0co30o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536356223877120/tumblr_njkq53Roep1t0co30o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536424121139210/tumblr_oalathnmFC1uskgfro1_400.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536451807739904/tumblr_nfg22lqmZ31rjwa86o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219536686529380362/tumblr_o98bm76djb1vv3oz0o1_500.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219537181440475146/tumblr_mya4mdVhDv1rmk3cyo1_500.gif',
                'https://i.imgur.com/4xnJN9x.png',
                'https://i.imgur.com/bunWIWD.jpg']
        msg = f'{random.choice(neps)}'
        embed = discord.Embed(title='NEP NEP NEP')
        embed.set_image(url=msg)
        await ctx.send(embed=embed)

    @commands.command(aliases=['погладить'])
    async def pat(self, ctx, member: discord.Member = None):
        '''Погладить кого-то
        -----------
        ~pat @CrazyCatz
        '''
        gifs = ['https://gfycat.com/PoisedWindingCaecilian',
                'https://cdn.awwni.me/sou1.jpg',
                'https://i.imgur.com/Nzxa95W.gifv',
                'https://cdn.awwni.me/sk0x.png',
                'https://i.imgur.com/N0UIRkk.png',
                'https://cdn.awwni.me/r915.jpg',
                'https://i.imgur.com/VRViMGf.gifv',
                'https://i.imgur.com/73dNfOk.gifv',
                'https://i.imgur.com/UXAKjRc.jpg',
                'https://i.imgur.com/dzlDuNs.jpg',
                'https://i.imgur.com/hPR7SOt.gif',
                'https://i.imgur.com/IqGRUu4.gif',
                'https://68.media.tumblr.com/f95f14437809dfec8057b2bd525e6b4a/tumblr_omvkl2SzeK1ql0375o1_500.gif',
                'https://i.redd.it/0ffv8i3p1vrz.jpg',
                'http://i.imgur.com/3dzA6OU.png',
                'http://i.imgur.com/vkFKabZ.jpg',
                'https://i.imgur.com/Lb4p20s.jpg',
                'https://cdn.awwni.me/snot.jpg',
                'https://i.imgur.com/5yEOa6u.jpg',
                'https://i.redd.it/dc7oebkfsetz.jpg']

        if member == ctx.me:
            msg = random.choice(gifs)
            embed = discord.Embed(title=f'{ctx.author.name} погладил тебя {member.name}')
            embed.set_image(url=msg)
            await ctx.send(embed=embed)
        elif member is not None:
            msg = random.choice(gifs)
            embed = discord.Embed(title=f'{ctx.author.name} погладил тебя {member.name}')
            embed.set_image(url=msg)
            await ctx.send(embed=embed)

    @commands.command(aliases=['rate', 'вайфу'])
    async def ratewaifu(self, ctx, *, waifuName: str):
        '''Rate my waifu
        -----------
        ~ratewaifu Sagiri
        '''
        waifu = waifuName.lower()
        bestWaifus = ['kobeni', 'emilia', 'shinobu', 'karen', 'shouko', 'shoko',
                      'minori', 'chidori', 'sagiri', 'mashiro', 'last order',
                      'saki', 'makoto', 'yui', 'nep', 'nepgear', 'taiga']
        trashWaifus = ['shino', 'rikka']
        #this lists are highly biased, but who cares ¯\_(ツ)_/¯
        if waifu in bestWaifus:
            rating = 10
        elif waifu in trashWaifus:
            rating = 0
        else:
            rating = hash(waifu) % 10

        if waifu == 'emilia':
            emoji = '<:Emilia:230684388084416512>'
        elif waifu == 'shinobu':
            emoji = '<:Shinobu:303302053688770561>'
        elif waifu == 'mashiro':
            emoji = '<:mashiro:266233568626343936>'
        elif waifu == 'sagiri':
            emoji = '<:Sagiri:407630432319045634>'
        elif waifu == 'nep' or waifu == 'neptunia' or waifu == 'nepgear':
            emoji = '<:nep:261230988758220822>'
        elif rating < 2:
            emoji = ':put_litter_in_its_place:'
        elif rating < 5:
            emoji = '<:k3llyLUL:341946977266827264>'
        elif rating < 7:
            emoji = '<:k3llyTHINK:341946932639432704>'
        elif rating < 9:
            emojis = ['<:faeGasm:298772756412104704>', '<:naroGasm:341200647741243393>']
            emoji = random.choice(emojis)
        elif rating < 10:
            emojis = ['<:kanoLewd:230662559458525185>', '<:fowShy:230662561580843008>', '<:mendoLewd:230662561169801216>']
            emoji = random.choice(emojis)
        elif rating == 10:
            emojis = ['<:okhand:335170448666918923>', '<:nepnep:314906910061101057>', '<:gaku:249970768786489345>', '<:faeWant:313430419661914113>']
            emoji = random.choice(emojis)

        msg = f'{emoji} Я оцениваю **{waifuName}** как **{rating}/10**'
        await ctx.send(msg)

    @commands.command(aliases=['анимэ'])
    async def anime(self, ctx, *, animeName: str):
        '''Ищет на AniList.co аниме
        Пример:
        -----------
        ~anime Mushishi
        '''
        api = 'https://graphql.anilist.co'
        query = '''
        query ($name: String){
          Media(search: $name, type: ANIME) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            synonyms
            format
            status
            episodes
            duration
            nextAiringEpisode {
              episode
            }
            averageScore
            meanScore
            source
            genres
            tags {
              name
            }
            studios(isMain: true) {
              nodes {
                name
              }
            }
            siteUrl
          }
        }
        '''
        variables = {
            'name': animeName
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api, json={'query': query, 'variables': variables}, headers = self.bot.userAgentHeaders) as r:
                if r.status == 200:
                    json = await r.json()
                    data = json['data']['Media']

                    embed = discord.Embed(color=ctx.author.top_role.colour)
                    embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                    embed.set_thumbnail(url=data['coverImage']['large'])
                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        embed.add_field(name='Название', value=data['title']['romaji'], inline=False)
                    else:
                        embed.add_field(name='Название', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)

                    #embed.add_field(name='Beschreibung', value=data['description'], inline=False)
                    if data['synonyms'] != []:
                        embed.add_field(name='Синонимы', value=', '.join(data['synonyms']), inline=True)

                    embed.add_field(name='Тип', value=data['format'].replace('_', ' ').title().replace('Tv', 'TV'), inline=True)
                    if data['episodes'] > 1:
                        embed.add_field(name='Эпизодов', value='{} по {} min'.format(data['episodes'], data['duration']), inline=True)
                    else:
                        embed.add_field(name='Длительность', value=str(data['duration']) + ' min', inline=True)

                    embed.add_field(name='Запуск', value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']), inline=True)
                    if data['endDate']['day'] == None:
                        embed.add_field(name='Релиз', value=data['nextAiringEpisode']['episode'] - 1, inline=True)
                    elif data['episodes'] > 1:
                        embed.add_field(name='Конец', value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']), inline=True)

                    embed.add_field(name='Статус', value=data['status'].replace('_', ' ').title(), inline=True)

                    try:
                        embed.add_field(name='Haupt-Studio', value=data['studios']['nodes'][0]['name'], inline=True)
                    except IndexError:
                        pass
                    embed.add_field(name='Ø Рейтнг', value=data['averageScore'], inline=True)
                    embed.add_field(name='Жанр', value=', '.join(data['genres']), inline=False)
                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    embed.add_field(name='Тэги', value=tags[:-2], inline=False)
                    try:
                        embed.add_field(name='Адаптировано из', value=data['source'].replace('_', ' ').title(), inline=True)
                    except AttributeError:
                        pass

                    embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                    embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(':x: Не удалось найти подходящее аниме!')

    @commands.command(aliases=['манга'])
    async def manga(self, ctx, *, mangaName: str):
        '''Ищет на AniList.co  мангу

        Пример:
        -----------
        ~manga Air Gear
        '''
        api = 'https://graphql.anilist.co'
        query = '''
        query ($name: String){
          Media(search: $name, type: MANGA) {
            id
            idMal
            description
            title {
              romaji
              english
            }
            coverImage {
              large
            }
            startDate {
              year
              month
              day
            }
            endDate {
              year
              month
              day
            }
            status
            chapters
            volumes
            averageScore
            meanScore
            genres
            tags {
              name
            }
            siteUrl
          }
        }
        '''
        variables = {
            'name': mangaName
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api, json={'query': query, 'variables': variables}, headers = self.bot.userAgentHeaders) as r:
                if r.status == 200:
                    json = await r.json()
                    data = json['data']['Media']

                    embed = discord.Embed(color=ctx.author.top_role.colour)
                    embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                    embed.set_thumbnail(url=data['coverImage']['large'])
                    if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                        embed.add_field(name='Titel', value=data['title']['romaji'], inline=False)
                    else:
                        embed.add_field(name='Titel', value='{} ({})'.format(data['title']['english'], data['title']['romaji']), inline=False)
                    #embed.add_field(name='Beschreibung', value=data['description'], inline=False)
                    if data['chapters'] != None:
                        # https://github.com/AniList/ApiV2-GraphQL-Docs/issues/47
                        embed.add_field(name='Глава', value=data['chapters'], inline=True)
                        embed.add_field(name='Ленты', value=data['volumes'], inline=True)
                    embed.add_field(name='Запуск', value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'], data['startDate']['year']), inline=True)
                    if data['endDate']['day'] != None:
                        embed.add_field(name='Конец', value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'], data['endDate']['year']), inline=True)
                    embed.add_field(name='Статус', value=data['status'].replace('_', ' ').title(), inline=True)
                    embed.add_field(name='Ø Рейтниг', value=data['averageScore'], inline=True)
                    embed.add_field(name='Жанры', value=', '.join(data['genres']), inline=False)
                    tags = ''
                    for tag in data['tags']:
                        tags += tag['name'] + ', '
                    embed.add_field(name='Tags', value=tags[:-2], inline=False)
                    embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                    embed.add_field(name='MyAnimeList Link', value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(':x: Не удалось найти подходящую мангу!')

    @commands.command()
    async def ser_ani(self, ctx, url: str = None):
        '''Пытается найти аниме по изображению

        Пример:
        -----------
        ~saucenao
        ~saucenao https://i.imgur.com/nmnVtgs.jpg
        '''
        
        if url == None:
            async for message in ctx.channel.history(before=ctx.message):
                try:
                    url = message.attachments[0].url
                    continue
                except IndexError:
                    pass
        elif not url.endswith(('.jpg', '.png', '.bmp', '.gif', '.jpeg')):
            await ctx.send(':x: Не указан правильный URL-адрес!')
            return

        tmp = await ctx.send(f'Попробуйте Источник изображения <{url}> найти ...')
        saucenao = f'http://saucenao.com/search.php?db=999&url={url}'
        async with aiohttp.ClientSession(headers = self.bot.userAgentHeaders) as cs:
            async with cs.get(saucenao) as r:
                #Thanks to https://github.com/MistressMamiya/hsauce_bot/blob/master/get_source.py
                content = await r.text()
                content = content.split('Низкие результаты сходства')[0] # Get rid of the low similarity results
                artist = re.search(r'<strong>Creator: <\/strong>(.*?)<br', content)
                anime = re.search(r'<strong>Material: <\/strong>(.*?)<br', content)
                characters = re.search(r'<strong>Characters: <\/strong><br \/>(.*?)<br \/></div>', content)
                pixiv = re.search(r'<strong>Pixiv ID: </strong><a href=\"(.*?)\" class', content)
                danbooru = re.search(r'<a href=\"https://danbooru\.donmai\.us/post/show/(\d+)\">', content)
                gelbooru = re.search(r'<a href=\"https://gelbooru\.com/index\.php\?page=post&s=view&id=(\d+)\">', content)
                yandere = re.search(r'<a href=\"https://yande\.re/post/show/(\d+)\">', content)
                konachan = re.search(r'<a href=\"http://konachan\.com/post/show/(\d+)\">', content)
                sankaku = re.search(r'<a href=\"https://chan\.sankakucomplex\.com/post/show/(\d+)\">', content)

        embed = discord.Embed()
        embed.set_footer(text='Provided by https://saucenao.com')
        embed.set_thumbnail(url=url)
        if anime:
            embed.add_field(name='Аниме', value=anime.group(1), inline=True)
        if artist:
            embed.add_field(name='Художник', value=artist.group(1), inline=True)
        if characters:
            embed.add_field(name='Характеры', value=str(characters.group(1)).replace('<br />', ', '), inline=True)
        if pixiv:
            embed.add_field(name='Pixiv Link', value=pixiv.group(1), inline=False)
        if danbooru:
            embed.add_field(name='Danbooru Link', value='https://danbooru.donmai.us/post/show/' + danbooru.group(1), inline=False)
        if gelbooru:
            embed.add_field(name='Gelbooru Link', value='https://gelbooru.com/index.php?page=post&s=view&id=' + gelbooru.group(1), inline=False)
        if yandere:
            embed.add_field(name='Yande.re Link', value='https://yande.re/post/show/' + yandere.group(1), inline=False)
        if konachan:
            embed.add_field(name='Konachan Link', value='http://konachan.com/post/show/' + konachan.group(1), inline=False)
        if sankaku:
            embed.add_field(name='Sankaku Link', value='https://chan.sankakucomplex.com/post/show/' + sankaku.group(1), inline=False)

        if anime or artist or characters or pixiv or danbooru or gelbooru or yandere or konachan or sankaku:
            await tmp.edit(content='', embed=embed)
        else:
            await tmp.edit(content=':x: Не удалось найти ничего!')


def setup(bot):
    bot.add_cog(anime(bot))
