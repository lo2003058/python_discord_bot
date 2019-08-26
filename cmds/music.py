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
queues = {}


class Music(Cog_Extension):

    @commands.command(pass_context=True)
    async def play(self, ctx, url: str = ""):
        # ------------------------------------connect ------------------------------------------------------#
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        # ------------------------------------------ download ----------------------------------------------------#
        path = "./music/youtube/song.mp3"
        song_there = os.path.isfile(path)
        try:
            if song_there:
                os.remove(path)

        except PermissionError:
            await ctx.send(F"try to delete song file,but it's being playing")
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./music/youtube"):
            if file.endswith(".mp3"):
                name = file
                os.rename(file, './music/youtube/song.mp3')
       # ------------------------------------------ play ----------------------------------------------------#
        voice.play(discord.FFmpegPCMAudio("./music/youtube/song.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.5

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]} - {nname[1]}")


@commands.command()
async def leave(self, ctx):
    global voice
    # channel = ctx.message.author.voice.channel

    # <discord.voice_client.VoiceClient object at 0x00000000054B4F28>
    voice = get(self.bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        print(voice)
        await voice.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))
