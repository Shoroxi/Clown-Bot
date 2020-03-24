import math
import random
import discord
import asyncio
import aiohttp
import loadconfig
from discord.ext import commands

class math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

def setup(bot):
    bot.add_cog(math(bot))