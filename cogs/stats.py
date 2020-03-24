import discord
import time
import io
from discord.ext import commands

#old code, y fix
cool = "```xl\n{0}\n```"
class Stats(commands.Cog):
  def __init__(self, bot):
    super().__init__(bot)
    self.cursor = bot.mysql.cursor
    self.queue_message = bot.queue_message
    self.discord_path = bot.path.discord
    self.files_path = bot.path.files

  @commands.command()
  async def updatestats(self):
    await self.update_stats()
    await self.carbon()
    await self.discord_pw()
    await self.bot.say(':white_check_mark: Upated Stats.')

  async def server_count(self):
    sql = 'SELECT * FROM `stats`'
    result = self.cursor.execute(sql).fetchall()
    count = 0
    for shard in result:
      count += int(shard['servers'])
    return count

  sent = 0
  key = ''
  API = 'https://www.carbonitex.net/discord/data/botdata.php'
  async def carbon(self):
    server_count = await self.server_count()
    data = {
      'key': self.key,
      'servercount': server_count,
      "botname": self.bot.user.name,
      "botid": self.bot.user.id,
      "logoid": self.bot.user.avatar_url[60:].replace(".jpg",""),
      "ownerid": '130070621034905600',
      "ownername": 'NotSoSuper'
    }

  async def on_server_join(self, server):
    await self.update_stats()
    await self.carbon()
    await self.discord_pw()

  async def on_server_leave(self, server):
    await self.update_stats()
    await self.carbon()
    await self.discord_pw()

  async def on_ready(self):
    await self.update_stats()
    await self.carbon()
    await self.discord_pw()

def setup(bot):
  bot.add_cog(Stats(bot))