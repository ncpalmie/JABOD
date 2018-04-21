import random

def pickTeams(member_list, team_number=2):
    members_not_picked = member_list
    member_list_size = len(member_list)
    members_per_team = member_list_size / team_number
    team_array = []
    for i in range(0, team_number):
        for m in range(0, members_per_team):
            new_team = []
            mem_index = random.randint(0, len(members_not_picked - 1))
            new_team.append(members_not_picked[mem_index])
            members_not_picked.pop(mem_index)
        team_array.append([new_team])
    return team_array
    