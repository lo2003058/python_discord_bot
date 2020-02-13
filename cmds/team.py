import discord
from discord import ChannelType
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random
import time

with open('conf/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

total_member_list = {}
total_orange_list = {}
total_blue_list = {}

global_create_team_message_id = 0
global_orange_team_message_id = 0
global_blue_team_message_id = 0


class Team(Cog_Extension):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cc"])
    async def change_channel(self, ctx):
        channel = ctx.message.author.voice.channel
        test_room = discord.utils.find(lambda g: g.name == channel.name, ctx.guild.channels)
        test_role = discord.utils.find(lambda g: g.id == 282900375261151232, ctx.guild.roles)
        orange_room = discord.utils.find(lambda g: g.id == 407486655638011905, ctx.guild.channels)
        blue_room = discord.utils.find(lambda g: g.id == 337216154416185346, ctx.guild.channels)
        for member in test_room.members:
            for role in member.roles:
                if role == test_role:
                    await member.move_to(orange_room)

        # orange_role = discord.utils.find(lambda g: g.id == 671330594315042818, ctx.guild.roles)
        # blue_role = discord.utils.find(lambda g: g.id == 671330927258894357, ctx.guild.roles)
        # channel = discord.utils.get(ctx.guild.channels, type=ChannelType.voice)

        # global voice
        # channel = ctx.message.author.voice.channel
        # voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # if voice and voice.is_connected():
        #     await voice.move_members(orange_room)
        # else:
        #     voice = await orange_room.connect()

    @commands.command(aliases=["pr"])
    async def print_test(self, ctx):
        global global_create_team_message_id
        global global_orange_team_message_id
        global global_blue_team_message_id
        global total_orange_list
        global total_blue_list
        global total_member_list
        print("global_create_team_message_id : " + str(global_create_team_message_id))
        print("global_orange_team_message_id : " + str(global_orange_team_message_id))
        print("global_blue_team_message_id : " + str(global_blue_team_message_id))
        print("total_orange_list : " + str(total_orange_list))
        print("total_blue_list : " + str(total_blue_list))
        print("total_member_list : " + str(total_member_list))

    @commands.command(aliases=["ctr"])
    async def clear_team_record(self, ctx):
        global global_create_team_message_id
        global global_orange_team_message_id
        global global_blue_team_message_id

        await ctx.send(content=F'Wait a minute')
        orange_role = discord.utils.find(lambda g: g.id == 671330594315042818, ctx.guild.roles)
        blue_role = discord.utils.find(lambda g: g.id == 671330927258894357, ctx.guild.roles)
        ready_role = discord.utils.find(lambda g: g.id == 671333863187808281, ctx.guild.roles)
        global_create_team_message_id = global_orange_team_message_id = global_blue_team_message_id = 0
        total_blue_list.clear()
        total_orange_list.clear()
        total_member_list.clear()

        for member in ready_role.members:
            print(F'Remove {member} in ready')
            await member.remove_roles(ready_role)
            time.sleep(2)

        for member in orange_role.members:
            print(F'Remove {member} in orange')
            await member.remove_roles(orange_role)
            time.sleep(2)

        for member in blue_role.members:
            print(F'Remove {member} in blue')
            await member.remove_roles(blue_role)
            time.sleep(2)

        await ctx.send(content=F'All clear')
        return global_create_team_message_id, global_orange_team_message_id, global_blue_team_message_id

    @commands.command(aliases=["ctb"])
    async def create_team_button(self, ctx, title='隨機分隊'):
        global global_create_team_message_id
        emoji = '<:lm12:283490998313811968>'
        embed = discord.Embed(title=title,
                              description="##############################",
                              color=0xffff80)
        embed.set_thumbnail(url="https://i.imgur.com/BJOrKbJ.gif")
        embed.add_field(name='同意請撳制', value=F'{emoji}', inline=True)
        last_message = await ctx.send(embed=embed)
        await last_message.add_reaction(':lm12:283490998313811968')
        global_create_team_message_id = ctx.channel.last_message_id
        return global_create_team_message_id

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global global_create_team_message_id
        global global_orange_team_message_id
        global global_blue_team_message_id
        global total_orange_list
        global total_blue_list
        orange_permission = False
        blue_permission = False
        role_status = False
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
        orange_room = discord.utils.find(lambda g: g.id == 407486655638011905, guild.channels)
        blue_room = discord.utils.find(lambda g: g.id == 337216154416185346, guild.channels)
        orange_role = discord.utils.find(lambda g: g.id == 671330594315042818, guild.roles)
        blue_role = discord.utils.find(lambda g: g.id == 671330927258894357, guild.roles)
        ready_role = discord.utils.find(lambda g: g.id == 671333863187808281, guild.roles)


        # 以message_id分辨function,分派身份組
        if message_id == global_create_team_message_id:
            if payload.emoji.name == 'lm12':
                role = ready_role
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None and member.bot is False:
                    total_member_list[payload.user_id] = payload.member.nick
                    await member.add_roles(role)
                    print('done')
                else:
                    print('Member not found')
            else:
                print('Role not found')
        elif message_id == global_blue_team_message_id:
            if payload.emoji.name == 'lm20' and message_id == global_blue_team_message_id:
                role = blue_role
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(member.roles)

                # 分辨成員的隊伍,橙只可撳橙,藍只可撳藍
                for member_info in total_blue_list:
                    if payload.user_id == member_info[0]:
                        blue_permission = True

                # 分辨成員是否已經有身份組
                for member_role in member.roles:
                    if member_role == blue_role:
                        role_status = True

                if member is not None and member.bot is False and blue_permission is True and role_status is False:
                    await member.remove_roles(ready_role)
                    time.sleep(3)
                    await member.add_roles(role)
                    time.sleep(5)
                    await member.move_to(blue_room)
                    print('done')
                else:
                    print('Member not found')
            else:
                print('Role not found')
        elif message_id == global_orange_team_message_id:
            if payload.emoji.name == 'lm20' and message_id == global_orange_team_message_id:
                role = orange_role
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(member.roles)

                # 分辨成員的隊伍,橙只可撳橙,藍只可撳藍
                for member_info in total_orange_list:
                    if payload.user_id == member_info[0]:
                        orange_permission = True

                # 分辨成員是否已經有身份組
                for member_role in member.roles:
                    if member_role == orange_role:
                        role_status = True

                if member is not None and member.bot is False and orange_permission is True and role_status is False:
                    await member.remove_roles(ready_role)
                    time.sleep(3)
                    await member.add_roles(role)
                    time.sleep(5)
                    await member.move_to(orange_room)
                    print('done')
                else:
                    print('Member not found')
            else:
                print('Role not found')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global global_create_team_message_id
        global global_orange_team_message_id
        global global_blue_team_message_id
        orange_permission = False
        blue_permission = False
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
        ready_role = discord.utils.get(guild.roles, name='準備中')

        # 以message_id分辨function,移除身份組
        if message_id == global_create_team_message_id:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == 'lm12':
                role = discord.utils.get(guild.roles, name='準備中')
            else:
                role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

                if member is not None and member.bot is False:
                    total_member_list.pop(payload.user_id)
                    await member.remove_roles(role)
                    print('done')
                else:
                    print('Member not found')
            else:
                print('Role not found')

        # 移除身份組,會有delay
        # elif message_id == global_blue_team_message_id:
        #     if payload.emoji.name == 'lm20' and message_id == global_blue_team_message_id:
        #         role = discord.utils.get(guild.roles, name='藍方')
        #     else:
        #         role = discord.utils.get(guild.roles, name=payload.emoji.name)
        #
        #     if role is not None:
        #         member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        #
        #         # 分辨成員的隊伍,橙只可撳橙,藍只可撳藍
        #         for member_info in total_blue_list:
        #             if payload.user_id == member_info[0]:
        #                 blue_permission = True
        #
        #         if member is not None and member.bot is False and blue_permission is True:
        #             await member.remove_roles(role)
        #             time.sleep(3)
        #             await member.add_roles(ready_role)
        #             print('done')
        #         else:
        #             print('Member not found')
        #     else:
        #         print('Role not found')
        # elif message_id == global_orange_team_message_id:
        #     if payload.emoji.name == 'lm20' and message_id == global_orange_team_message_id:
        #         role = discord.utils.get(guild.roles, name='橙方')
        #     else:
        #         role = discord.utils.get(guild.roles, name=payload.emoji.name)
        #
        #     if role is not None:
        #         member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        #
        #         # 分辨成員的隊伍,橙只可撳橙,藍只可撳藍
        #         for member_info in total_orange_list:
        #             if payload.user_id == member_info[0]:
        #                 orange_permission = True
        #
        #         if member is not None and member.bot is False and orange_permission is True:
        #             await member.remove_roles(role)
        #             time.sleep(3)
        #             await member.add_roles(ready_role)
        #             print('done')
        #         else:
        #             print('Member not found')
        #     else:
        #         print('Role not found')

    @commands.command(aliases=["tr"])
    async def test_r(self, ctx, total_member=0):
        test_total_member_list = {
            1876876786: 'test1',
            2865168464: 'test2',
            3783153437: 'test3',
            4783456476: 'test4',
            5378378378: 'test5',
            6373287378: 'test6',
            7123456772: 'test7',
            8123467887: 'test8',
            9237837833: 'test9',
            243371252704739329: 'Yin  (求職廢青)',
        }

        global total_member_list
        total_member_list = test_total_member_list
        shuffle_list = list(test_total_member_list.items())
        # random.shuffle(shuffle_list)

        if len(test_total_member_list) <= total_member:
            if len(test_total_member_list) % 2 == 0:
                global total_orange_list
                global total_blue_list
                orange_list = random.sample(shuffle_list, k=5)
                for data in orange_list:
                    shuffle_list.remove(data)
                blue_list = shuffle_list

                total_orange_list = orange_list
                total_blue_list = blue_list

                # orange_list = shuffle_list[0:5]
                # blue_list = shuffle_list[5:]
                # total_orange_list = orange_list
                # total_blue_list = blue_list

                orange_num = blue_num = 1
                global global_orange_team_message_id
                emoji = '<:lm20:567188297638608914>'
                embed = discord.Embed(title='橙方隊員',
                                      description="##################################",
                                      color=0xff9933)
                embed.set_thumbnail(url="https://i.imgur.com/lEmLVLH.gif")
                embed.add_field(name='準備請撳', value=F'{emoji}', inline=True)
                for member in orange_list:
                    embed.add_field(name=str(orange_num), value=F'{member[1]}', inline=True)
                    orange_num += 1

                embed = await ctx.send(embed=embed)
                await embed.add_reaction(':lm20:567188297638608914')
                global_orange_team_message_id = ctx.channel.last_message_id
                time.sleep(2)
                await ctx.send(content=F'============準備後五秒自動轉房============')

                global global_blue_team_message_id
                emoji = '<:lm20:567188297638608914>'
                embed = discord.Embed(title='藍方隊員',
                                      description="##################################",
                                      color=0x0066ff)
                embed.set_thumbnail(url="https://i.imgur.com/lEmLVLH.gif")

                embed.add_field(name='準備請撳', value=F'{emoji}', inline=True)
                for member in blue_list:
                    embed.add_field(name=str(blue_num), value=F'{member[1]}', inline=True)
                    blue_num += 1

                message_id = await ctx.send(embed=embed)
                await message_id.add_reaction(':lm20:567188297638608914')
                global_blue_team_message_id = ctx.channel.last_message_id

                return global_orange_team_message_id, global_blue_team_message_id, total_orange_list, total_blue_list, total_member_list

            else:
                await ctx.send(content=F'{len(shuffle_list)}人分唔到兩隊')
        else:
            await ctx.send(content=F'凸咗{len(shuffle_list) - total_member}個人分唔到隊')


def setup(bot):
    bot.add_cog(Team(bot))
