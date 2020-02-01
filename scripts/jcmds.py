import discord, random, asyncio, utility
from discord.ext import commands

class Player:
    pid = 0
    def __init__(self, member):
        self.member = member
        self.score = 0
        self.pid = Player.pid
        Player.pid += 1

class PictionaryPicture:
    picture_list = None
    def __init__(self, names, content=""):
        self.names = names
        self.content = content

def setup_pictionary():
    if PictionaryPicture.picture_list != None:
        return picture_list
    line_index = 0
    ret_picture_list = []
    ascii_file = open('../config/ascii_art.txt', 'r')
    ascii_file_lines = ascii_file.readlines()
    ascii_file.close()

    while (line_index < len(ascii_file_lines)):
        if ascii_file_lines[line_index] == "//\n":
            image_strs = []
            line_index += 1
            new_picture = PictionaryPicture(ascii_file_lines[line_index])
            line_index += 1
            while line_index < len(ascii_file_lines) and ascii_file_lines[line_index] != "//\n":
                image_strs.append(ascii_file_lines[line_index])
                line_index += 1
            new_picture.content = image_strs
        ret_picture_list.append(new_picture)
    PictionaryPicture.picture_list = ret_picture_list
    return ret_picture_list

async def chamber_member(client, member_name):
    rand_voice_channel = utility.get_random_voice_channel(client)
    main_guild = utility.get_main_guild(client)
    channel = utility.get_main_text_channel(main_guild)
    if utility.is_member_in_channel(client, member_name):
        member = utility.get_channel_member_by_name(client, member_name)
        await member.edit(voice_channel=rand_voice_channel)
        await JABOD.play_audio('../sounds/confirm/okay.mp3', rand_voice_channel)
    else:
        await channel.send("That member is not in a voice channel")

async def pictionary(client, challenger_name, challenged_name):
    picture_list = setup_pictionary()
    curr_round = 0
    main_guild = utility.get_main_guild(client)
    main_channel = utility.get_main_text_channel(main_guild)
    player1 = Player(utility.get_channel_member_by_name(client, challenger_name))
    player2 = Player(utility.get_channel_member_by_name(client, challenged_name))
    while (curr_round != 6):
        await main_channel.send('==========================================================')
        await main_channel.send("Pictionary Round " + str(curr_round))
        await main_channel.send("Player " + player1.member.name + " has " + str(player1.score) + " points")
        await main_channel.send("Player " + player2.member.name + " has " + str(player2.score) + " points")
        await main_channel.send("Begin Guessing")

        #Run round and begin outputting picture line by line
        picture_index = 0
        current_picture = ""
        picture = picture_list[random.randint(0, len(picture_list))]
        valid_words = picture.names.split(",")
        solved = False
        while (picture_index < len(picture.content)):
            current_picture += picture.content[picture_index]
            await main_channel.send('==========================================================')
            await main_channel.send(current_picture)
            #Check for messages which contain the correct response
            async for message in main_channel.history(limit=20):
                if message.author == player1.member and message.content in valid_words:
                    await main_channel.send("Player " + player1.member.name + " got it! " + message.content)
                    player1.score += len(picture.content) - picture_index
                    solved = True
                    picture_index = len(picture.content)
                if message.author == player2.member and message.content in valid_words:
                    await main_channel.send("Player " + player2.member.name + " got it! " + message.content)
                    player2.score += len(picture.content) - picture_index
                    solved = True
                    picture_index = len(picture.content)
            picture_index += 1
            print(valid_words[0])
        if not solved:
            await main_channel.send("No one got it! It's a " + valid_words[0])
        curr_round += 1
    #Finish game and output score/winner
    if player1.score > player2.score:
        await main_channel.send("Player " + player1.member.name + " wins with " + str(player1.score) + " points!")
    elif player1.score == player2.score:
        await main_channel.send("Players tie at " + str(player1.score) + " points!")
    else:
        await main_channel.send("Player " + player2.member.name + " wins with " + str(player1.score) + " points!")

async def bounce_member(client, member_name, bounces):
    member = None
    if bounces > 10:
        bounces = 10
    if member_name == None:
        member = utility.get_random_channel_member(client)
    else:
        member = utility.get_channel_member_by_name(client, member_name)
    for i in range(0, bounces):
        await member.edit(voice_channel=utility.get_random_voice_channel(client))

