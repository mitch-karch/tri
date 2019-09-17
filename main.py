from brain import externalCall
import sys
import json
from random import random

default_config = {
                "WIDTH": 1920,
                "HEIGHT": 1080,
                "BLEED_X": 200,
                "BLEED_Y": 200,
                "CELL_SIZE": 190,
                "VARIANCE": 50,
                "RAND_FN": "random",
                "color_steps": 20,
                "FIRST_COLOR": "#FEBF01",
                "SECOND_COLOR": "#FF02F6",
                "THIRD_COLOR": "#444444",
                "FOURTH_COLOR": "#FFFFFF"
                }


def main():
    global default_config
    loadConfig()

    if(default_config["RAND_FN"] == "random"):
        default_config["RAND_FN"] = random

    externalCall(default_config, save_bg=True)

def loadConfig():
    global default_config
    if len(sys.argv) == 2:
        # Expected argument:
        # Name of JSON file
        with open(sys.argv[1]) as json_file:
            default_config = json.load(json_file)

main()
