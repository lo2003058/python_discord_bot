from discord.ext import commands
from core.classes import Cog_Extension
import discord
import time
import random
import json

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        time.sleep(0.5)
        if message.content == "香港警察":
            message = random.choice(jdata['hkpopo'])
            string = message[:4]
            emoji = message[4:]
            await channel.send(F"{string} {emoji}")
        elif message.content == "警察OT":
            string = '老婆3P'
            emoji = '<:lm24:567189614775762951>'
            await channel.send(F"{string} {emoji}")
        elif message.content == "光復香港":
            string = '時代革命'
            emoji = '<:lm3:283490996963115008>'
            await channel.send(F"{string} {emoji}")

def setup(bot):
    bot.add_cog(Event(bot))
