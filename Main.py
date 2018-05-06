import discord
from discord.ext import commands
from feudanfrans import *
from random_funcs import *
import random
import time

TOKEN = 'NDM3MzY1MDY5MjI4Mjc3NzYy.Db0_ig.xab3yTZvjt2LjoHvLTKUaYENP9g'

client = discord.Client()

@client.event
async def on_message(message):
    member = message.author
    server = member.server
    if member.name == 'crizm' and 'make teams' in message.content:
        team_string = pickTeams(server.members, message.content)
        await client.send_message(message.channel, 'Teams made')
        for string in team_string:
            await client.send_message(message.channel, string)
            
    elif member.name == 'crizm' and 'leave' in message.content:
        await client.send_message(message.channel, 'Goodbye')
        await client.close()
        
    elif member.name == 'crizm' and 'parse prompt' in message.content:
        for string in parseTextFile('qanda.txt')[1]:
            await client.send_message(message.channel, string)

    elif message.content.startswith('play odds'):
        info_arr = playOdds(message)
        await client.send_message(server, "Playing odds with low of " + info_arr[0] + " and high of " + info_arr[1])
        await client.send_message(server, "I will start counting down from three when you type 'ready'...")
        await client.wait_for_message(timeout=10,author=message.author,content='ready')
        await client.send_message(server, '3')
        time.sleep(0.8)
        await client.send_message(server, '2')
        time.sleep(0.8)
        await client.send_message(server, '1')
        time.sleep(0.8)
        await client.send_message(server, info_arr[2])
        
#@client.event
#async def on_voice_state_update(member, voice_state):
#    if member.name == "crizm":
#        await client.send_message(member.server, "Kildax you are in the wrong channel, get your shit together")
    

@client.event
async def on_member_remove(member):
    if member.name == 'Khryonex':
        await client.send_message(member.server, 'Oh good, the talking cheese is gone')
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)