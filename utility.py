import discord, random, asyncio
from discord.ext import commands

def get_random_channel_member(client):
    member_pool = []
    voice_channels = get_main_guild(client).voice_channels
    for voice_channel in voice_channels:
        for member in voice_channel.members:
            member_pool.append(member)
    chosen_member = member_pool[random.randint(0, len(member_pool) - 1)]
    return chosen_member

def get_channel_member_by_name(client, member_name):
    ret_member = None
    member_name = member_name.lower()
    voice_channels = get_main_guild(client).voice_channels
    for voice_channel in voice_channels:
        for member in voice_channel.members:
            if member.name.lower() == member_name:
                ret_member = member
    return ret_member

def is_member_in_channel(client, member_name, voice_channel=None):
    if voice_channel == None:
        if get_channel_member_by_name(client, member_name) != None:
            return True
        return False
    else:
        for member in voice_channel.members:
            if member.name == member_name:
                return True
        return False

def get_random_voice_channel(client):
    main_guild = get_main_guild(client)
    return main_guild.voice_channels[random.randint(0, len(main_guild.voice_channels) - 1)]

def get_voice_channel_by_name(client, name):
    main_guild = get_main_guild(client)
    for voice_channel in main_guild.voice_channels:
        if voice_channel.name.lower() == name.lower():
            return voice_channel
    return None

def get_main_guild(client):
    for guild in client.guilds:
        if guild.name == "Something Sweeter":
            return guild

def get_main_text_channel(main_guild):
    for text_channel in main_guild.text_channels:
        if text_channel.name == "general":
            return text_channel

def print_in_channel_member_names(client):
    voice_channels = get_main_guild(client).voice_channels
    for voice_channel in voice_channels:
        for member in voice_channel.members:
            print(member.name)

