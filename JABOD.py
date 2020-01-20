import discord
from discord.ext import commands
import debug
import random
import time

TOKEN = 'NDM3MzY1MDY5MjI4Mjc3NzYy.Db0_ig.xab3yTZvjt2LjoHvLTKUaYENP9g'
client = discord.Client()

#Setup commands to run
command_file = open("debug_commands.txt", 'r')
commands = command_file.readlines()

@client.event
async def execute_commands(client):
    main_guild = None
    main_channel = None
    for guild in client.guilds:
        if guild.name == "Something Sweeter":
            main_guild = guild
    for text_channel in main_guild.text_channels:
        if text_channel.name == "general":
            main_channel = text_channel
    await debug.parse_commands(client, commands, main_channel)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await execute_commands(client)

client.run(TOKEN)
