import discord
from discord.ext import commands
from feudanfrans import *
import random

TOKEN = 'NDM3MzY1MDY5MjI4Mjc3NzYy.Db0_ig.xab3yTZvjt2LjoHvLTKUaYENP9g'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_message(message):
    member = message.author
    if member.name == 'crizm' and message.content.startswith('ay'):
        await client.send_message(message.channel, 'Goodbye')
        await client.close()
        
@client.event
async def on_message(message):
    member = message.author
    guild = member.guild
    if member.name == 'crizm' and 'make teams' in message.content:
        pickTeams(guild.members)
        await client.send_message('Teams made')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)