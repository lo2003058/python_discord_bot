import discord
from discord.ext import commands
import os
import json

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix=".")


@bot.event
async def on_ready():
    print(">> Bot is online <<")


@bot.command()
async def load(ctx, extension):
    if jdata['roles']['Bot Tester'] in [str(role.id) for role in ctx.author.roles]:
        bot.load_extension(F'cmds.{extension}')
        await ctx.channel.purge(limit=1)
        emoji = '<:lm23:567189028131045401>'
        await ctx.send(F'幫你Load好{extension}了{emoji} ')
    else:
        emoji = '<:lm8:283490997059715073>'
        await ctx.send(F'你係冇特權,冇得大撚哂{emoji}')


@bot.command()
async def unload(ctx, extension):
    if jdata['roles']['Bot Tester'] in [str(role.id) for role in ctx.author.roles]:
        bot.unload_extension(F'cmds.{extension}')
        await ctx.channel.purge(limit=1)
        emoji = '<:lm23:567189028131045401>'
        await ctx.send(F'幫你Unload咗{extension}了{emoji}')
    else:
        emoji = '<:lm8:283490997059715073>'
        await ctx.send(F'你係冇特權,冇得大撚哂{emoji}')


@bot.command()
async def reload(ctx, extension):
    if jdata['roles']['Bot Tester'] in [str(role.id) for role in ctx.author.roles]:
        bot.reload_extension(F'cmds.{extension}')
        await ctx.channel.purge(limit=1)
        emoji = '<:lm23:567189028131045401>'
        await ctx.send(F'幫你Reload咗{extension}了{emoji}')
    else:
        emoji = '<:lm8:283490997059715073>'
        await ctx.send(F'你係冇特權,冇得大撚哂{emoji}')


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(F'cmds.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['token'])
