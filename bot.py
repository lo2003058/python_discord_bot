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
    bot.load_extension(F'cmds.{extension}')
    await ctx.send(F'Loaded {extension} done.')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(F'cmds.{extension}')
    await ctx.send(F'Unloaded {extension} done.')


@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(F'cmds.{extension}')
    await ctx.send(F'Reloaded {extension} done.')


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(F'cmds.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['token'])
