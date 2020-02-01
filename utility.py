from __future__ import unicode_literals
from discord.ext import commands
from bs4 import BeautifulSoup
import os, time, asyncio
import jcmds
import discord
import youtube_dl
import random
import urllib.request

class Watchdog:
    def __init__(self, client):
        self.client = client
        self.main_text_channel = None
        self.last_check_message = None
        self.this_check_message = None
        self.members_in_vcs = []
    """Watches for specific changes in channel to
    break loop and handle awaited events. Some events
    may be checked less often than others due to lower
    priority than voice control. Only events that can
    have some effect on JABOD are currently watched."""
    def watch(self):
        #Can't be in init since watchdog is made prior to client activation
        if self.main_text_channel == None:
            main_guild = get_main_guild(self.client)
            self.main_text_channel = get_main_text_channel(main_guild)
        #Check if new message has appeared in the channel
        self.this_check_message = self.main_text_channel.last_message
        if self.this_check_message == None:
            return False
        if self.last_check_message == None or self.this_check_message.id != self.last_check_message.id:
            self.last_check_message = self.this_check_message
            return True
        self.last_check_message = self.this_check_message
        #Check if member has joined a voice channel
        #if self.members_in_vcs == [] or self.members_in_vcs != get_speaking_members(self.client):
        #    self.members_in_vcs = get_speaking_members(self.client)
        #    return True
        return False
        
def get_random_channel_member(client):
    member_pool = []
    voice_channels = get_main_guild(client).voice_channels
    for voice_channel in voice_channels:
        for member in voice_channel.members:
            member_pool.append(member)
    chosen_member = member_pool[random.randint(0, len(member_pool) - 1)]
    return chosen_member

def get_speaking_members(client):
    voice_channels = get_main_guild(client).voice_channels
    ret_list = []
    for voice_channel in voice_channels:
        for member in voice_channel.members:
            ret_list.append(member)
    return ret_list

def get_channel_member_by_name(client, member_name):
    ret_member = None
    member_name = member_name.lower()
    voice_channels = get_main_guild(client).voice_channels
    for voice_channel in voice_channels:
        for member in voice_channel.members:
            if member.name.lower() == member_name:
                ret_member = member
    return ret_member

def get_vc_with_member(client, member_name):
    main_guild = get_main_guild(client)
    for voice_channel in main_guild.voice_channels:
        for member in voice_channel.members:
            if member.name.lower() == member_name.lower():
                return voice_channel
    return None

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

def get_random_sound(folder_name):
    sounds_dir = "./sounds/" + folder_name + "/"
    sounds = os.listdir(sounds_dir)
    return sounds_dir + sounds[random.randint(0, len(sounds)-1)]

async def parse_commands(client, commands, text_channel):
    for command in commands:
        command_args = command.split(',')
        if "sendMsg" in command_args[0]:
            await text_channel.send(command_args[1])
        if "bounce" in command_args[0]:
            await jcmds.bounce_member(client, None, int(command_args[1]))
        if "play" in command_args[0]:
            mp3_file = get_mp3_file(get_video_link(command_args[0][4:]))
            await play_vc_audio(client.voice_clients[0], mp3_file)
            os.remove(mp3_file)

async def play_vc_audio(client, audio_file_name):
    vc = client.voice_clients[0]
    vc_stopped = False
    vc.play(discord.FFmpegPCMAudio(audio_file_name))
    while vc.is_playing() and not vc_stopped:
        text_channel = get_main_text_channel(get_main_guild(client))
        if text_channel.last_message != None and text_channel.last_message.content.lower() == "stop":
            vc_stopped = True
        await asyncio.sleep(1)
    vc.stop()

def get_video_link(video_name):
    query = urllib.parse.quote(video_name)
    search_url = "https://www.youtube.com/results?search_query=" + query
    search_html = urllib.request.urlopen(search_url).read()
    soup = BeautifulSoup(search_html, 'html.parser')
    videos = soup.findAll(attrs={'class':'yt-uix-tile-link'})
    if len(videos) > 0:
        top_video = videos[0]
    else:
        print("Nothing found")
    return "https://www.youtube.com" + top_video['href']
        
def get_mp3_file(video_link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([str(video_link)])
    for _file in os.listdir():
        if "mp3" in _file:
            return _file
    return None
