import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json, asyncio, datetime


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def setup(bot):
    bot.add_cog(Task(bot))
