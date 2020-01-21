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

def get_random_voice_channel(client):
    main_guild = get_main_guild(client)
    return main_guild.voice_channels[random.randint(0, len(main_guild.voice_channels) - 1)]

def get_main_guild(client):
    for guild in client.guilds:
        if guild.name == "Something Sweeter":
            return guild

def get_main_text_channel(main_guild):
    for text_channel in main_guild.text_channels:
        if text_channel.name == "general":
            return text_channel

async def bounce_member(client, member_name, bounces):
    member = None
    if bounces > 10:
        bounces = 10
    if member_name == None:
        member = get_random_channel_member(client)
    else:
        member = get_member_by_name(member_name)
    for i in range(0, bounces):
        await member.edit(voice_channel=get_random_voice_channel(client))