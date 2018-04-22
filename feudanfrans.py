import random

def pickTeams(member_list, team_number=2):
    members_not_picked = []
    for value in member_list:
        members_not_picked.append(value)
    member_list_size = len(member_list)
    members_per_team = member_list_size // team_number
    team_array = []
    return_array = []
    for i in range(0, team_number):
        new_team = []
        for m in range(0, members_per_team):
            mem_index = random.randint(0, len(members_not_picked) - 1)
            new_team.append(members_not_picked[mem_index])
            members_not_picked.pop(mem_index)
        team_array.append([new_team])
    for team_list in team_array:
        team = []
        for extra_array in team_list:
            for member in extra_array:
                #if member.status == 'online':
                    team.append(member)
        return_array.append(team)
    return return_array
    
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
