import discord
from discord.ext import commands
import utility

async def parse_commands(client, commands, text_channel):
    for command in commands:
        command_args = command.split(',')
        if command_args[0] == "-sendMsg":
            await text_channel.send(command_args[1])
        if command_args[0] == "-bounce":
            await utility.bounce_member(client, None, int(command_args[1]))
