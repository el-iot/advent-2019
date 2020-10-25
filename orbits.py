import collections
import json

import requests

URL = "https://adventofcode.com/2019/day/6/input"

with open("cookies.json", "r") as file:
    cookies = json.load(file)

text = requests.get(URL, cookies=cookies).text
orbits = collections.defaultdict(list)

for line in text.split("\n"):

    if not line:
        continue

    [big, small] = line.split(")")
    orbits[big].append(small)
    orbits[small].append(big)

orbits = dict(orbits)

queue = [("YOU", [], {*()})]
paths = []

while queue:

    new, path, seen = queue.pop(0)

    if new == "SAN":
        paths.append(path + [new])
        continue

    if new in seen:
        continue

    seen |= {new}

    for newer in orbits.get(new, []):
        queue.append((newer, path + [new], seen))

print(">> %s" % (min(len(path) for path in paths) - 3))
