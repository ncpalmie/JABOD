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
    if member.name == 'crizm' and 'make teams' == message.content:
        team_string = pickTeams(server.members, message.content)
        await client.send_message(message.channel, 'Teams made')
        for string in team_string:
            await client.send_message(message.channel, string)
            
    elif member.name == 'crizm' and 'start Feudan\' Frans' == message.content:
        await client.send_message(server, 'Starting Feudan Frans...')
        await client.send_message(server, 'Input name of gamemaster: ')
    
    elif member.name.lower() == 'crizm' and 'make teams+' == message.content:
        team_string = pickTeams(server.members, message.content)
        for team in team_string:
            teammate_str = team[8:]
            teammate_arr = teammate_str.split(', ')
            for teammate in teammate_arr:
                await move_mem(server, teammate, 'FF-Team' + team[5])
        
            
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
        
    elif 'move(' in message.content and 'Owner' in get_name_list(member.roles):
        args_str = message.content[5:len(message.content) - 1]
        args_list = args_str.split(', ')
        await move_mem(server, args_list[0], args_list[1])
        
    elif 'debug' in message.content:
        await client.send_message(server, member.roles[1].name)
        
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
    
@client.event
async def move_mem(server, member_name, channel_name):
    chan_dict = get_channel_dict()
    member_dict = get_member_dict()
    try:
        await client.move_member(member_dict[member_name], chan_dict[channel_name])
    except KeyError:
        await client.send_message(server, 'No online, channel-bound member has the nickname: ' + member_name)
    
    
def get_channel_dict():
    avail_channels = client.get_all_channels()
    channel_dict = {}
    for channel in avail_channels:
        channel_dict[str(channel)] = channel
    return channel_dict
    
def get_member_dict():
    avail_members = client.get_all_members()
    member_dict = {}
    for member in avail_members:
        if str(member.status) == 'online':
            member_dict[member.name.lower()] = member
    return member_dict
    
def get_name_list(list_given):
    return_list = []
    for item in list_given:
        return_list.append(item.name)
    return return_list


client.run(TOKEN)
