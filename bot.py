import discord
import time
import random
import config
import asyncio
import math
import aiohttp
import json
from discord import utils
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Game


class MyClient(discord.Client):
    async def on_ready(self):
        activity1 = ["С ЛЮДЬМИ","Fuck"]
        activity = discord.Game(name = (random.choice(activity1)), type=3)
        await client.change_presence(status=discord.Status.idle, activity=activity)
        await asyncio.sleep(3)
        print("Bot online")

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
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

    async def on_message(self, message):
        if message.content == '!hello':
            msg = 'Hello {0.author.mention}'.format(message)
            await message.channel.send(msg)
        if message.content == "square":
            await message.channel.send("Введите число, которое вы хотите возвести в квадрат")
            x = float(input())
            xs =  x*x
            await message.channel.send(xs)    

client = MyClient()
client.run(config.TOKEN)
