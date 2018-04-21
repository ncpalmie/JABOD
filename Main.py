import discord
from discord.ext import commands
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
async def on_voice_state_update(member, voice_state):
    if member.name == 'crizm' and voice_state.self_deaf:
	await client.close()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)