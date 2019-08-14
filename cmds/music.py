import discord
from discord.ext import commands
from discord.utils import get
from core.classes import Cog_Extension
import json
import youtube_dl
import os
import time

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

players = {}


class Music(Cog_Extension):

    @commands.command()
    async def play(self, ctx, link: str = ""):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)


        print(channel)
        print(voice)


        # if link:
        #     if voice and voice.is_connected():
        #         await voice.move_to(channel)
        #
        #         # ydl_opts = {
        #         #     'format': 'bestaudio/best',
        #         #     'postprocessors': [{
        #         #         'key': 'FFmpegExtrractAudio',
        #         #         'preferredcodec': 'mp3',
        #         #         'preferredquality': '192',
        #         #     }]
        #         # }
        #         # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #         #     print("Downloading audio now\n")
        #         #     ydl.download([link])
        #         # for file in os.listdir("./music/youtube"):
        #         #     if file.endswith(".mp3"):
        #         #         name = file
        #         #         print(F"rename file:{file}\n")
        #         #         os.rename(file, "song.mp3")
        #
        #         player = await voice.create_ytdl_player(link)
        #         players[channel] = player
        #         player.start()
        #
        #
        #     else:
        #         voice = await channel.connect()
        #         player = await voice.create_ytdl_player(link)
        #         players[channel] = player
        #         player.start()
        # else:
        #     emoji = '<:lm22:567188971063345166>'
        #     await ctx.send(F'冇link點播呀{emoji}')

    @commands.command()
    async def leave(self, ctx):
        global voice
        # channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))
