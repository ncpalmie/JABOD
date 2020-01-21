import discord
from discord.ext import commands
import debug, math, random, time, utility

TOKEN = 'NDM3MzY1MDY5MjI4Mjc3NzYy.XiY9Lw.h8OOAe0kjuDMWmdZ_JaTTlPl2R0'
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
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await execute_commands(client)

client.run(TOKEN)
