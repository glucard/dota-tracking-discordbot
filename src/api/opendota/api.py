from urllib.error import HTTPError
import requests

def getPlayer(account_id):
    params = {
        'account_id':account_id
    }
    r = requests.get(f"https://api.opendota.com/api/players/{account_id}")

    if r.status_code != 200:
        raise HTTPError
    
    return r.json()

def getRecentMatches(account_id):
    params = {
        'account_id':account_id
    }
    r = requests.get(f"https://api.opendota.com/api/players/{account_id}/recentMatches")

    if r.status_code != 200:
        raise HTTPError
    
    return r.json()