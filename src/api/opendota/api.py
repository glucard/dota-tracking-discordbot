from urllib.error import HTTPError
import requests

def getPlayer(account_id):
    r = requests.get(f"https://api.opendota.com/api/players/{account_id}")

    if r.status_code != 200:
        raise HTTPError()
    
    return r.json()
    
def getHeroes():
    r = requests.get("https://api.opendota.com/api/heroes")

    if r.status_code != 200:
        raise HTTPError()
    
    return r.json()

def getMatch(match_id):
    r = requests.get(f"https://api.opendota.com/api/matches/{match_id}")

    if r.status_code != 200:
        raise HTTPError()
    
    return r.json()

def getRecentMatches(account_id):
    r = requests.get(f"https://api.opendota.com/api/players/{account_id}/recentMatches")

    if r.status_code != 200:
        raise HTTPError()
    
    return r.json()

def getMatchResume(match_id):
    get_match = getMatch(match_id)
    match = {}
    match = {
        'radiant_win': get_match['radiant_win'],
        'duration': get_match['duration'],
        'start_time': get_match['start_time'],
        'players': {}
    }
    i = 0
    for player in get_match['players']:
        i+=1
        account_id = str(player['account_id']) if player['account_id'] != None else f"private-{i}"
        match['players'][account_id] = {
            'account_id': account_id,
            'assists': player['assists'],
            'deaths': player['deaths'],
            'denies': player['denies'],
            'hero_damage': player['hero_damage'],
            'hero_id': player['hero_id'],
            'kills': player['kills'],
            'last_hits': player['last_hits'],
            'level': player['level'],
            'net_worth': player['net_worth'],
            'sen_placed': player['sen_placed'],
            'tower_damage': player['tower_damage'],
            'xp_per_min': player['xp_per_min'],
            'obs_placed': player['obs_placed'],
        }
    return match