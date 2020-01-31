
from discord.ext import commands
from discord.ext.commands import Bot
from discord import utils
import config
import discord
import random
import time
import asyncio


gay = ['100%! да ты бомба', '99% -_-.. а где уй в жопе?', '93%', '91%',  '89%',  '87%',  '85%',  '83%','81%', '79%', '77%', '75%', '73%', '71%', '69%', '67%', '65%', '63%', '60%', '59%', '57%',  '55%',  '53%', '51%', '50% истинный баланс', '49% а дотянуть не мог а?', '48%а дотянуть не мог а?', '47%', '45%', '43%', '42%', '40%', '38%', '36%', '34%', '32%',  '30%', '28%',  '26%',  '24%', '22%',  '20%',  '18%',  '16%',  '14%',  '12%',  '10%', '9% ты на грани', '8% ты на грани', '7% ты на грани', '6% ты на грани', '5% ты на грани', '4% ты на грани', '3% ты на грани', '2% ты на грани', '1% ты на грани', '0% кажется тебе здесь не место']



class DiscordBot(discord.Client):
    async def on_ready(self):
        print('Discord bot in online!')
        activity = discord.Game(name="🔥Ready For ShreX🔥")
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message):
        # don't respond to ourselves
    
        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content =='xtoya':
            await message.channel.send('u is a trap')

        if message.content == 'howgay':
            await message.channel.send(random.choice(gay))
            

        if message.content == 'Удаляй сервак к чертям':
            await message.channel.send('Как скажете, повелитель')
            time.sleep(5)
            await message.channel.send ("10")
            time.sleep(1)
            await message.channel.send("9")
            time.sleep(1)
            await message.channel.send('8')
            time.sleep(1)
            await message.channel.send('7')
            time.sleep(1)
            await message.channel.send('6')
            time.sleep(1)
            await message.channel.send('5')
            time.sleep(1)
            await message.channel.send('4')
            time.sleep(1)
            await message.channel.send('3')
            time.sleep(1)
            await message.channel.send('2')
            time.sleep(1)
            await message.channel.send('1')
            time.sleep(1)
            await message.channel.send('0')
            time.sleep(1)
            await message.channel.send('fuck this gay Earth')

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
       
            if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))
       
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
 
    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
 
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
 


client = DiscordBot()
client.run(config.TOKEN)