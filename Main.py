import discord
from discord.ext import commands
from feudanfrans import *
import random

TOKEN = 'NDM3MzY1MDY5MjI4Mjc3NzYy.Db0_ig.xab3yTZvjt2LjoHvLTKUaYENP9g'

client = discord.Client()

@client.event
async def on_message(message):
    member = message.author
    guild = member.server
    if member.name == 'crizm' and 'make teams' in message.content:
        if message.content[len(message.content) - 1].isnumeric():
            team_list = pickTeams(guild.members, int(message.content[len(message.content) - 1]))
        else:
            team_list = pickTeams(guild.members)
        team_string = toString('teams', team_list)
        await client.send_message(message.channel, 'Teams made')
        for string in team_string:
            await client.send_message(message.channel, string)
    elif member.name == 'crizm' and 'leave' in message.content:
        await client.send_message(message.channel, 'Goodbye')
        await client.close()

@client.event
async def on_member_remove(member):
    if member.name == 'Khryonex':
        await client.send_message(member.channel, 'Oh good, the talking cheese is gone')
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)