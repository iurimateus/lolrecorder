import model
import handler
import helper

import requests
import re
import sys
import os

from time import sleep
from typing import List, Dict, Pattern
from datetime import datetime


def init():
    file_name = "summoners.json"

    data: List[Dict[str, str]] = model.load_from_json(file_name)
    players: model.Players = model.Players(data)

    collection: List[model.Player] = players.players

    len_collection = len(collection)

    if len_collection <= 0:
        print("No players found...")
        return

    while True:
        msg = f"Checking {len_collection} players..."

        time = f"{datetime.now():%Y, %b %d - %H:%M:%S}"
        print(f"{time}: {msg}")

        for player in collection:
            main_loop(player)
            sleep(0.5)

        sleep(120)
        print()


def main_loop(player: model.Player) -> None:
    player.print()

    schema = "http"
    region = player.region_code
    host = "op.gg"

    url = f"{schema}://{region}.{host}"

    spectate_url = f"{url}/summoner/spectator/userName={player.name}"
    record_url = f"{url}/summoner/ajax/requestRecording/gameId="

    try:
        spectate_url = requests.utils.requote_uri(spectate_url)
        response = requests.get(spectate_url)
    except Exception as err:
        print(f"\nException: {err}\n")
        return

    if response.status_code == 200:
        body: str = response.text
        if helper.canRecord(body):
            # Pattern matches a game id. Example:
            # 'requestRecording(this, '1561011980');'
            # match: 1561011980
            pattern = re.compile(r".requestRecording\(this, '(\d+)'\)")
            match = pattern.search(body)
            if not match:
                return

            game_id = match.groups()[0]  # grab first group

            print("\n\tSending request...", end="")

            record_url = f"{record_url}{game_id}"
            try:
                response = requests.get(record_url)
                if response.status_code == 200:
                    body: str = response.text
                    if "The game has been saved to OP.GG" in body:
                        print("Success!")
            except Exception as err:
                print("Failed with err:\n\t", err)


if __name__ == "__main__":
    init()
