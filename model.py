from typing import List, Dict
import json


# A Player must have a region code and a name
class Player:
    name: str
    region_code: str

    def __init__(self, name: str, region_code: str) -> None:
        if not valid_region_prefix(region_code):
            raise Exception("Invalid region prefix")

        self.name = name
        self.region_code = check_korea_code(region_code)

    def print(self) -> None:
        region = code_to_region(self.region_code)
        print(f"{self.name:<16} - {region:<20}", end="")


# Players class is a collection of 'player' objects
class Players:
    players: List[Player]

    def __init__(self, players: List[Player]) -> None:
        self.players = players

    def save(self, file_name: str) -> None:
        lst: List[Dict[str, str]] = list(dict())
        for obj in self.players:
            # Decode obj into a list of dictionaries to make it JSON compatible
            dct: Dict[str, str] = dict()

            dct["name"] = obj.name
            dct["region_code"] = obj.region_code

            lst.append(dct)

        data = {"summoners": lst}

        try:
            with open(file_name, "w") as f:
                json.dump(data, f, indent=2, sort_keys=True)
        except Exception as err:
            print("\nPlayers: Error while saving to disk.")
            print(err)

    def add(self, player: Player):
        name = player.name
        region_code = check_korea_code(player.region_code)

        if valid_name(name) and valid_region_prefix(region_code):
            self.players.append(player)

    def print(self) -> None:
        for player in self.players:
            player.print()
            print()


def load_from_json(file_name: str) -> Players:
    # Encode obj from JSON as a Summoner class
    def as_summoner(obj: Dict[str, str]) -> Player:
        if "name" in obj:
            return Player(obj["name"], obj["region_code"])
        return obj

    with open(file_name) as f:
        data = json.load(f, object_hook=as_summoner)
        return data['summoners']


# Names must be at least 3 characters long and no more than 16 characters long.
# https://support.riotgames.com/hc/en-us/articles/201752814-Summoner-Name-FAQ
def valid_name(name: str) -> bool:
    return 3 <= len(name) <= 16


def valid_region_prefix(prefix: str) -> bool:
    region_prefixes: List[str] = [
        "na", "eune", "euw",
        "br", "lan", "las",
        "oce", "ru", "jp",
        "tr", "www"
    ]

    return prefix in region_prefixes


# Maps region_prefix/code to a readable name.
def code_to_region(region_prefix: str) -> str:
    if not valid_region_prefix(region_prefix):
        raise ValueError("Invalid region prefix ", region_prefix)

    code_to_region: Dict[str, str] = {
        "na": "North America",
        "eune": "Europe Noridc & East",
        "euw": "Europe West",
        "br": "Brazil",
        "lan": "Latin America North",
        "las": "Latin America South",
        "oce": "Oceania",
        "ru": "Russia",
        "jp": "Japan",
        "tr": "Turkey",
        "www": "Korea",
    }

    return code_to_region[region_prefix]


# For ease of use, maps 'kr' to 'www'
def check_korea_code(code: str) -> str:
    if code == "kr":
        code = "www"

    return code
