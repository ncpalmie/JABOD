import os, sys, math, random, time, asyncio, subprocess
import discord
import jcmds
import utility as util
import audio_util as au
from discord.ext import commands
from os import path

tkn_file = open("../config/JABOD.token", "r")
tkn = tkn_file.readline()
tkn_file.close()

TOKEN = tkn[0:-1]
client = discord.Client()
voice_watchdog = util.Watchdog(client)

#Setup commands to run
command_file = open("../debug_commands.txt", 'r')
commands = command_file.readlines()
command_file.close()

#"Randomize" seed
random.seed(math.floor(time.time()))

async def execute_commands(client, file_name):
    main_guild = util.get_main_guild(client)
    main_channel = util.get_main_text_channel(main_guild)
    command_file = open(file_name, 'r')
    commands = command_file.readlines()
    command_file.close()
    await util.parse_commands(client, commands, main_channel)

async def voice_poll(client, voice_watchdog):
    while True:#not voice_watchdog.watch():
        if path.exists("trigger.file"):
            os.remove("trigger.file")
            vc = await util.get_vc_with_member(client, "crizm").connect()
            await au.play_vc_audio(client, au.get_random_sound("depressing"))
            record = subprocess.Popen([sys.executable, "record.py"])
            while record.poll() == None:
                pass
            record.kill()
            translate = subprocess.Popen([sys.executable, "translate.py"])
            while translate.poll() == None:
                pass
            translate.kill()
            if path.exists("voice_cmd.txt"):
                await execute_commands(client, "voice_cmd.txt")
                os.remove("voice_cmd.txt")
            await au.play_vc_audio(client, au.get_random_sound("depressing"))
            os.remove("speech.wav")
            await asyncio.sleep(2)
            await vc.disconnect()    

#this should break stuff to show you this
#erm
#oh yeah
#implement it so that double mute in short time pulls you
#into individual channel to ask for your request
#then spits you and JABOD back, try to be careful with the
#vcs to stop whatever causes him to restart. this overall
#should be just way better than voice, maybe even consider removing
#voice but idk if they'd use it still yk

@client.event
async def on_voice_state_update(member, before, after):
    if util.Watchdog.previous_time == None:
        util.Watchdog.previous_member = member
        util.Watchdog.previous_time = time.time()
    elif member == util.Watchdog.previous_member and time.time() - util.Watchdog.previous_time < 1:
        util.Watchdog.previous_member = member
        util.Watchdog.previous_time = time.time()
        vc = await util.get_vc_with_member(client, "crizm").connect()
        await au.play_vc_audio(client, au.get_random_sound("depressing"))
        record = subprocess.Popen([sys.executable, "record.py"])
        while record.poll() == None:
            pass
        record.kill()
        translate = subprocess.Popen([sys.executable, "translate.py"])
        while translate.poll() == None:
            pass
        translate.kill()
        if path.exists("voice_cmd.txt"):
            await execute_commands(client, "voice_cmd.txt")
            os.remove("voice_cmd.txt")
        await au.play_vc_audio(client, au.get_random_sound("depressing"))
        os.remove("speech.wav")
        await asyncio.sleep(2)
        await vc.disconnect()    

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    channel = message.channel
    if content[0] != "$":
        return
    #Admin only commands
    if 'admin' in str(author.top_role):
        command_args = content[1:].split(' ')
        #Bounce
        if 'bounce' in command_args[0] and len(command_args) == 3:
            if util.is_member_in_channel(client, command_args[1]):
                await jcmds.bounce_member(client, command_args[1], int(command_args[2]))
            else:
                await channel.send("That member is not in a voice channel")
        #Scream Chamber
        elif 'scream' in command_args[0] and len(command_args) == 2:
            rand_voice_channel = util.get_random_voice_channel(client)
            main_guild = util.get_main_guild(client)
            channel = util.get_main_text_channel(main_guild)
            if util.is_member_in_channel(client, command_args[1]):
                member = util.get_channel_member_by_name(client, command_args[1])
                await member.edit(voice_channel=rand_voice_channel)
                await au.play_audio('../sounds/confirm/okay.mp3', rand_voice_channel)
            else:
                await channel.send("That member is not in a voice channel")
        #Summon
        elif 'summon' in command_args[0] and len(command_args) == 1:
            #Add summon code    
            pass
        #Pictionary
        elif 'pictionary' in command_args[0] and len(command_args) == 2:
            if author.name == command_args[1]:
                await channel.send("You cannot play pictionary against yourself")
            else:
                if util.is_member_in_channel(client, command_args[1]):
                    await jcmds.pictionary(client, author.name, command_args[1])
                else:
                    await channel.send("That member is not in a voice channel")
    print('done')
#    await voice_poll(client, voice_watchdog)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await execute_commands(client, "../debug_commands.txt")
    #await voice_poll(client, voice_watchdog)
    #REMOVE LATER
    #main_guild = util.get_main_guild(client)
    #print(util.get_main_text_channel(main_guild).last_message.content)

client.run(TOKEN)
