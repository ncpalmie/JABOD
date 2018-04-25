import random
import math

def pickTeams(member_list, message_request):
    if message_request[len(message_request) - 1].isnumeric():
        team_number = int(message_request[len(message_request) - 1])
    members_not_picked = []
    return_array = []
    for member in member_list:
        if str(member.status) == 'online' and not member.bot:
            members_not_picked.append(member)
    for x in range(0, team_number):
        return_array.append([])
    num_per_team = math.ceil(len(members_not_picked) / team_number)
    while len(members_not_picked) > 0 and not allTeamsFull(return_array, num_per_team):
        team_index = random.randint(0, len(return_array) - 1)
        if len(return_array[team_index]) < num_per_team:
            return_array[team_index].append(members_not_picked[0])
            members_not_picked.pop(0)
    str_array = toString('teams', return_array)
    return str_array
    
def allTeamsFull(team_list, num_per_team):
     for team in team_list:
        if len(team) < num_per_team:
            return False
     return True
    
def toString(label, optional=None):
    if label == 'teams':
        str_array = []
        index = 1
        for team in optional:
            team_string = 'TEAM ' + str(index) + ': '
            for member in team:
                team_string += member.name + ', '
            team_string = team_string[0:len(team_string) - 2]
            str_array.append(team_string)
            index += 1
        return str_array
        
def parseTextFile(filename):
    #Reads a file of the below format and places prompts and answers into matching spots in seperate arrays
    #Format:
    #The first letter of every line will not be included, it is being used as an identifier
    #Lines that are prompts should start with an exclamation point, lines following should start with a number that decides
    #the order of the answers when they are displayed, a single equals sign is used to denote the end of a questions
    #At the end of an answer, there should be a dash with the number of points given to it immediately following
    #I.E.
    #!Name an occupation that you'd want your enemy to have.
    #1Garbage Collector-54
    #2Prison Guard-23
    #3Fast-Food Worker-6
    #=
    feud_file = open(filename, 'r')
    feud_text = feud_file.readlines()
    q_and_a_sets = []
    for line in feud_text:
        feud_text[feud_text.index(line)] = line.rstrip()
    for index in range(0, len(feud_text)):
        temp_arr = []
        if feud_text[index][0] == '!':
            temp_arr.append(feud_text[index][1:])
            orig_index = index
            while feud_text[index + 1][0].isnumeric():
                index += 1
            temp_arr.append(feud_text[orig_index + 1:index + 1])
            loop_int = 0
            for answer in temp_arr[1]:
                temp_arr[1][loop_int] = temp_arr[1][loop_int][1:]
                loop_int += 1
            print(temp_arr)
        if len(temp_arr) > 0:    
            q_and_a_sets.append(temp_arr)
    return q_and_a_sets
    

    

    
    
    
    
    
    
    
    
    
    
    
    