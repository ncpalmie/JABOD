from __future__ import unicode_literals
from discord.ext import commands
from bs4 import BeautifulSoup
import os, time, asyncio
import utility as util
import discord
import youtube_dl
import random
import urllib.request

async def play_vc_audio(client, audio_file_name):
    vc = client.voice_clients[0]
    vc_stopped = False
    vc.play(discord.FFmpegPCMAudio(audio_file_name))
    while vc.is_playing() and not vc_stopped:
        text_channel = util.get_main_text_channel(util.get_main_guild(client))
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

def get_random_sound(folder_name):
    sounds_dir = "../sounds/" + folder_name + "/"
    sounds = os.listdir(sounds_dir)
    return sounds_dir + sounds[random.randint(0, len(sounds)-1)]

async def play_audio(audio_file_name, voice_channel):
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(audio_file_name))
    while vc.is_playing():
        await asyncio.sleep(1)
    vc.stop()
    await vc.disconnect()    
