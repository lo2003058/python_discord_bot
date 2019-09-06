import discord
from discord.ext import commands
from discord.utils import get
from core.classes import Cog_Extension
import json
import youtube_dl
import os
import shutil

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

players = {}
queues = {}
music_playlist = []


class Music(Cog_Extension):

    @commands.command(pass_context=True, aliases=["p"])
    async def play(self, ctx, url: str = ""):

        def check_queue():
            Queue_infile = os.path.isdir("./music/queue")
            if Queue_infile is True:
                dir = "./music/queue"
                length = len(os.listdir(dir))
                still_q = length - 1
                try:
                    first_file = os.listdir(dir)[0]
                except:
                    queues.clear()
                    return
                main_location = "./music/youtube"
                song_path = "./music/queue" + "/" + first_file
                if length != 0:
                    print("Song done,playing next queued\n")
                    song_there = os.path.isfile('./music/youtube/song.mp3')
                    if song_there:
                        os.remove('./music/youtube/song.mp3')
                    shutil.move(song_path, main_location)
                    music_playlist.pop(0)
                    for file in os.listdir("./music/youtube"):
                        if file.endswith(".mp3"):
                            os.rename('./music/youtube/' + file, './music/youtube/song.mp3')

                    voice.play(discord.FFmpegPCMAudio('./music/youtube/song.mp3'),
                               after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)

                else:
                    queues.clear()
                    return
            else:
                queues.clear()

        def add_to_queue():
            Queue_infile = os.path.isdir("./music/queue")
            print(Queue_infile)
            if Queue_infile is False:
                os.mkdir("./music/queue")
            dir = "./music/queue"
            q_num = len(os.listdir(dir))
            q_num += 1
            add_queue = True
            while add_queue:
                if q_num in queues:
                    q_num += 1
                else:
                    add_queue = False
                    queues[q_num] = q_num

            # queue_path = "./music/queue/%(title)s.%(ext)s"

            ydl_opts = {
                'format': 'bestaudio/best',
                #'outtmpl': queue_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.download([url])

            for file in os.listdir('./'):
                if file.endswith(".mp3"):
                    name = file
                    os.rename(file, f'./music/queue/song{q_num}.mp3')
            nname = name.rsplit("-", 2)
            music_playlist.append(nname[0] + '-' + nname[1])

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
                queues.clear()
        except PermissionError:
            add_to_queue()
            emoji = '<:lm20:567188297638608914>'
            await ctx.send(F"加咗入條list,排緊隊{emoji}")
            return

        queue_infile = os.path.isdir("./music/queue")
        try:
            queue_folder = "./music/queue"
            if queue_infile is True:
                print("removed old queue folder")
                shutil.rmtree(queue_folder)
        except:
            print("No old queue folder")

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

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                os.rename(file, './music/youtube/song.mp3')
        # ------------------------------------------ play ----------------------------------------------------#
        nname = name.rsplit("-", 2)
        music_playlist.append(nname[0] + '-' + nname[1])
        voice.play(discord.FFmpegPCMAudio("./music/youtube/song.mp3"),
                   after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)

        # await ctx.send(f"播緊 : {nname[0]}-{nname[1]}")

    @commands.command(pass_context=True, aliases=["ml"])
    async def musiclist(self, ctx):

        #testlist = ['美波「ライラック」MV-GQ3V50XoLOM.mp3', '美波「ホロネス」MV-HIRiduzNLzQ.mp3', '美波「カワキヲアメク」MV-0YF8vecQWYs.mp3']

        count = 0
        if music_playlist:
            embed = discord.Embed(title="歌list",
                                  description="##################################",
                                  color=0xffff80)
            embed.set_thumbnail(url="https://i.imgur.com/lEmLVLH.gif")
            for music in music_playlist:
                if count == 0:
                    embed.add_field(name='播放中', value=f'{music}', inline=False)
                else:
                    embed.add_field(name=f'#{count}', value=f'{music}', inline=False)

                count += 1
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'無歌邊有Playlist')

    @commands.command()
    async def test(self, ctx):
        print(music_playlist)

    @commands.command()
    async def leave(self, ctx):
        global voice
        # channel = ctx.message.author.voice.channel
        # <discord.voice_client.VoiceClient object at 0x00000000054B4F28>
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            print(voice)
            music_playlist.clear()
            await voice.disconnect()

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print('Music pause')
            voice.pause()
            await ctx.send('歌已暫停')
        else:
            print("Music not playing")
            await ctx.send('無歌點暫停')

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print('Resume music')
            voice.resume()
            await ctx.send('繼續播')
        else:
            print("Music not pause")
            await ctx.send('無歌點繼續播')

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        queues.clear()

        if voice and voice.is_playing():
            print('Music stopped')
            voice.stop()
            await ctx.send('歌已Cut')
        else:
            print("no msuic to stop")
            await ctx.send('無歌點Cut')

    # @commands.command(pass_context=True, aliases=["q"])
    # async def queue(self, ctx, url: str = ""):
    #     Queue_infile = os.path.isdir("./music/queue")
    #     print(Queue_infile)
    #     if Queue_infile is False:
    #         os.mkdir("./music/queue")
    #     dir = "./music/queue"
    #     # dir = os.path.path("./music/queue")
    #     q_num = len(os.listdir(dir))
    #     q_num += 1
    #     add_queue = True
    #     while add_queue:
    #         if q_num in queues:
    #             q_num += 1
    #         else:
    #             add_queue = False
    #             queues[q_num] = q_num
    #
    #     queue_path = "./music/queue" + f"\song{q_num}.%(ext)s"
    #
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'outtmpl': queue_path,
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         }],
    #     }
    #
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         print("Downloading audio now\n")
    #         ydl.download([url])
    #     await ctx.send("加咗入條list,排緊隊")
    #
    #     print("song added to queue\n")


def setup(bot):
    bot.add_cog(Music(bot))
