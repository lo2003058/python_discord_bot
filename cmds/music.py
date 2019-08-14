import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import time

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Music(Cog_Extension):

    @commands.command()
    async def play(self, ctx):
        print('test')


def setup(bot):
    bot.add_cog(Music(bot))
