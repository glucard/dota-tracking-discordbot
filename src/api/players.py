# todo: fazer backups 
#       update players using threads.
from webbrowser import get
from .opendota import api
import json, time
import os.path

players_filename = "players.json"

unposted_matches = {} # new matches not posted.

medals = {
    '1': "Aroldão",
    '2': "Guardião",
    '3': "Cruzado",
    '4': "Arconte",
    '5': "Francis",
    '6': "Ancenstral",
}

def loadHeroes() -> dict:
    """load heroes names in a dict hero_id"""

    # if exist file heroes, load it.
    if os.path.exists("heroes.json"):
        f = open("heroes.json", encoding="utf8")
        heroes = json.load(f)
        f.close()
        return heroes

    # if not exist file heroes, then create one
    get_heroes = api.getHeroes() # query heroes 
    heroes = {}
    for hero in get_heroes:
        heroes[hero['id']] = hero['localized_name']

    with open("heroes.json", 'w', encoding='utf-8') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=4)
    
    return heroes
    

def loadPlayers() -> dict:
    """ If already exist file players, load it then return its content
        else return a empty dict """
    if os.path.exists(players_filename):
        f = open(players_filename, encoding="utf8")
        players = json.load(f)
        f.close()
        return players
    return {}

def insertPlayer(account_id) -> None:
    """ query a player and its recent matches by account_id in opendota api
        then store it in players dict  """
    players[account_id] = api.getPlayer(account_id)
    players[account_id]['recent_matches'] = api.getRecentMatches(account_id)  # fetch and insert recent matches
    players[account_id]['get_timestamp'] = time.time() # store instant timestamp

    # update players file
    with open(players_filename, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=4)

def getPlayer(account_id) -> dict:
    """ return a player by account_id """

    print(f"Loading player {account_id}:")
    
    # if player not exist, then call insertPlayer()
    if account_id not in players.keys():
        print(" - Inserting from api...")
        insertPlayer(account_id)

    # if the player exist, but it's outdate, then call insertPlayer().
    # Simultaneously, update unposted_matches list, inserting the new detected matches.
    if time.time() - players[account_id]['get_timestamp'] >= 60*5:
        print(" - Updating from api...")
        last_recent_matchs_id = [match['match_id'] for match in players[account_id]['recent_matches']] # store recent_matches_id before update player.
        insertPlayer(account_id) # update player
        recent_matchs_id = [match['match_id'] for match in players[account_id]['recent_matches']] # store updated recent_matches_id

        for match_id in reversed(recent_matchs_id): # reversed to adjust chronologic order.
            # if match_id not existed before, then add it to unspoted_matches list
            if match_id not in last_recent_matchs_id and match_id not in unposted_matches.keys():
                unposted_matches[match_id] = api.getMatchResume(match_id)

    # print name loaded.
    name = players[account_id]['profile']['personaname']
    print(f"{name} loaded.")

    return players[account_id]

def updateThread(interval) -> None:
    """ update all players 
        on a predetermined interval to prevent overload opendota api"""
    for p in players.keys():
        getPlayer(p)
        time.sleep(interval)
    

def medalScores() -> list:
    """ return all medals from inserted players """
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

players = loadPlayers() # load players
heroes = loadHeroes()   # load heroes