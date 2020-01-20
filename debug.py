import discord
from discord.ext import commands

async def parse_commands(client, commands, text_channel):
    for command in commands:
        command_args = command.split(',')
        if command_args[0] == "-sendMsg":
            await text_channel.send(command_args[1])
