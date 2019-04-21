# LOL Recorder

Based on https://github.com/tripleko/open-lol-recorder. Simple python script to
send requests for a game to be recorded on [OP.GG](https://www.op.gg/).

Every two minutes a record request will be sent to the players on
`summoners.json`.

## Running

`git clone https://github.com/iurimateus/lolrecorder.git`  
`cd lolrecorder`  
`python main.py`

Player name and region code must be specified as in `summoners.json` file.  
Region code follows op.gg prefixes.

### Requirements

Python 3.7+ with requests lib.
