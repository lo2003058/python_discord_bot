import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import time

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class React(Cog_Extension):

    @commands.command()
    async def seed(self, ctx):
        count = 0
        emoji = '<:lm4:283490996749205506>'
        await ctx.send(content=F"{ctx.author.mention}{emoji}")
        time.sleep(0.5)

        for image_data in jdata['images']:
            count = count + 1
            image = discord.File(image_data)
            await ctx.send(file=image)
            time.sleep(0.5)

        time.sleep(5)
        await ctx.channel.purge(limit=count + 1)

    @commands.command()
    async def live(self, ctx, num=6):
        if num > 24:
            num = 24
        emoji = '<:lm3:283490996963115008>'
        await ctx.send(F'{ctx.author.mention}光復香港 時代革命{emoji}')
        await ctx.send(F'https://ncehk2019.github.io/nce-live/?visibleCount={num}')


def setup(bot):
    bot.add_cog(React(bot))
