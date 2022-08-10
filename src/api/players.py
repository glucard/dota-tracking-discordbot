# todo: fazer backups 
#       update players using threads.
import opendota.api

import json, time
import os.path

players_filename = "players.json"

medals = {
    '1': "Aroldão",
    '2': "Guardião",
    '3': "Cruzado",
    '4': "Arconte",
    '5': "Francis",
    '6': "Ancenstral",
}

def loadPlayers():
    if os.path.exists(players_filename):
        f = open(players_filename, encoding="utf8")
        players = json.load(f)
        f.close()
        return players
    return {}

def insertPlayer(account_id):
    players[account_id] = opendota.api.getPlayer(account_id)
    players[account_id]['recent_matches'] = opendota.api.getRecentMatches(account_id)
    players[account_id]['get_timestamp'] = time.time()

def getPlayer(account_id):
    print(f"Loading player {account_id}:")
    
    if account_id not in players.keys():
        print(" - Inserting from api...")
        insertPlayer(account_id)

    if time.time() - players[account_id]['get_timestamp'] >= 60*5:
        print(" - Updating from api...")
        insertPlayer(account_id)

    name = players[account_id]['profile']['personaname']
    print(f"{name} loaded.")
    return players[account_id]

def updateThread(interval, max_time):
    while True:
        for p in players.keys():
            if time.time() - players[p]['get_timestamp'] > max_time:
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
############################


getPlayer('1124993606')

getPlayer('215795170')

getPlayer('359491712')

print(medalScores())



##########################################################
with open(players_filename, 'w', encoding='utf-8') as f:
    json.dump(players, f, ensure_ascii=False, indent=4)