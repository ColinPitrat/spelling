#!/usr/bin/python3

import json
import os
import subprocess
import sys


def say(phrase):
    my_env = os.environ
    my_env["SILENT_SAY"] = "true"
    phrase = phrase.replace("!", ".")
    phrase = '"' + phrase + '"'
    subprocess.call(["./say.sh", phrase])


if len(sys.argv) < 2:
    print("Syntax: %s <json file> [<json file> ...]")

for file in sys.argv[1:]:
    words = json.load(open(file))
    for word in words.keys():
        print(word)
        say(word)
