import os, requests

UA = {"User-Agent": "SkatlazWorldSportsMCP/1.0"}

class TheSportsDB:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("THESPORTSDB_API_KEY", "3")
        self.base = f"https://www.thesportsdb.com/api/v1/json/{self.api_key}"

    def search_team(self, name):
        r = requests.get(f"{self.base}/searchteams.php", params={"t": name}, headers=UA, timeout=20)
        r.raise_for_status()
        return r.json().get("teams") or []

    def search_player(self, name):
        r = requests.get(f"{self.base}/searchplayers.php", params={"p": name}, headers=UA, timeout=20)
        r.raise_for_status()
        return r.json().get("player") or []

    def next_events(self, team_id):
        r = requests.get(f"{self.base}/eventsnext.php", params={"id": team_id}, headers=UA, timeout=20)
        r.raise_for_status()
        return r.json().get("events") or []

class FootballData:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FOOTBALL_DATA_API_KEY", "")
        self.base = "https://api.football-data.org/v4"

    def _headers(self):
        h = dict(UA)
        if self.api_key:
            h["X-Auth-Token"] = self.api_key
        return h

    def competitions(self):
        r = requests.get(f"{self.base}/competitions", headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json()

    def standings(self, competition_code="PL"):
        r = requests.get(f"{self.base}/competitions/{competition_code}/standings", headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json()
