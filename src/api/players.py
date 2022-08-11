# todo: fazer backups 
#       update players using threads.
from webbrowser import get
from .opendota import api
import json, time
import os.path

players_filename = "players.json"
unposted_matchs = {}

medals = {
    '1': "Aroldão",
    '2': "Guardião",
    '3': "Cruzado",
    '4': "Arconte",
    '5': "Francis",
    '6': "Ancenstral",
}

def loadHeroes():

    if os.path.exists("heroes.json"):
        f = open("heroes.json", encoding="utf8")
        heroes = json.load(f)
        f.close()
        return heroes

    get_heroes = api.getHeroes()
    heroes = {}

    for hero in get_heroes:
        heroes[hero['id']] = hero['localized_name']
    with open("heroes.json", 'w', encoding='utf-8') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=4)
    
    return heroes
    

def loadPlayers():
    if os.path.exists(players_filename):
        f = open(players_filename, encoding="utf8")
        players = json.load(f)
        f.close()
        return players
    return {}

def insertPlayer(account_id):

    players[account_id] = api.getPlayer(account_id)
    players[account_id]['recent_matches'] = api.getRecentMatches(account_id)
    players[account_id]['get_timestamp'] = time.time()
    with open(players_filename, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=4)

def getPlayer(account_id):
    print(f"Loading player {account_id}:")
    
    if account_id not in players.keys():
        print(" - Inserting from api...")
        insertPlayer(account_id)

    if time.time() - players[account_id]['get_timestamp'] >= 60*5:
        print(" - Updating from api...")
        last_recent_matchs_id = [match['match_id'] for match in players[account_id]['recent_matches']]
        insertPlayer(account_id)
        recent_matchs_id = [match['match_id'] for match in players[account_id]['recent_matches']]

        for match_id in reversed(recent_matchs_id): # reversed to adjust chronologic order.
            if match_id not in last_recent_matchs_id and match_id not in unposted_matchs.keys():
                unposted_matchs[match_id] = api.getMatchResume(match_id)

    name = players[account_id]['profile']['personaname']
    print(f"{name} loaded.")
    return players[account_id]

def updateThread(interval):
    for p in players.keys():
        getPlayer(p)
        time.sleep(interval)
    

def medalScores():
    players_medal = []
    for p in players.keys():
        rank_tier = str(players[p]['rank_tier'])
        personaname = players[p]['profile']['personaname']
        medal = medals[rank_tier[:1]]+' '+str(rank_tier[1:])
        players_medal.append({
            'personaname':personaname,
            'medal':medal,
        })
    return players_medal

players = loadPlayers()
heroes = loadHeroes()
############################

"""
getPlayer('1124993606')

getPlayer('215795170')

getPlayer('359491712')
"""

##########################################################