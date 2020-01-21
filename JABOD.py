import discord
from discord.ext import commands
import debug, math, random, time, utility, asyncio

TOKEN = 'NDM3MzY1MDY5MjI4Mjc3NzYy.XiZLbA.IG6HqAuHog6FFCYc3M7N3igPLb0'
client = discord.Client()

#Setup commands to run
command_file = open("debug_commands.txt", 'r')
commands = command_file.readlines()

#"Randomize" seed
random.seed(math.floor(time.time()))

@client.event
async def execute_commands(client):
    main_guild = utility.get_main_guild(client)
    main_channel = utility.get_main_text_channel(main_guild)
    await debug.parse_commands(client, commands, main_channel)

@client.event
async def play_audio(audio_file_name, voice_channel):
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(audio_file_name))
    while vc.is_playing():
        await asyncio.sleep(1)
    vc.stop()
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
            if utility.is_member_in_channel(client, command_args[1]):
                await utility.bounce_member(client, command_args[1], int(command_args[2]))
            else:
                await channel.send("That member is not in a voice channel")
        #Scream Chamber
        elif 'scream' in command_args[0] and len(command_args) == 2:
            rand_voice_channel = utility.get_random_voice_channel(client)
            if utility.is_member_in_channel(client, command_args[1]):
                member = utility.get_channel_member_by_name(client, command_args[1])
                await member.edit(voice_channel=rand_voice_channel)
                await play_audio('scream.mp3', rand_voice_channel)
            else:
                await channel.send("That member is not in a voice channel")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await execute_commands(client)

client.run(TOKEN)
