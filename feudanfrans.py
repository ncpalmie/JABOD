import random
import math

def pickTeams(member_list, team_number=2):
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
    return return_array
    
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