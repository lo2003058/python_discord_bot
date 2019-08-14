import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Main(Cog_Extension):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(F'Ping : {round(self.bot.latency * 1000)} ')

    @commands.command()
    async def sayd(self, ctx, *, msg=""):
        if jdata['roles']['Bot Tester'] in [str(role.id) for role in ctx.author.roles]:
            if msg:
                await ctx.message.delete()
                await ctx.send(msg)
            else:
                emoji = '<:lm3:283490996963115008>'
                await ctx.send(F'你係咪唔識入字呀{emoji}')
        else:
            emoji = '<:lm8:283490997059715073>'
            await ctx.send(F'你係冇特權,冇得大撚哂{emoji}')

    @commands.command()
    async def clear(self, ctx, num: int = 0):
        if jdata['roles']['Bot Tester'] in [str(role.id) for role in ctx.author.roles]:
            if num >= 1:
                await ctx.channel.purge(limit=num + 1)
            else:
                emoji = '<:lm3:283490996963115008>'
                await ctx.send(F'係咪唔識入數字呀{emoji}')
        else:
            emoji = '<:lm8:283490997059715073>'
            await ctx.send(F'你係冇特權,冇得大撚哂{emoji}')


def setup(bot):
    bot.add_cog(Main(bot))
