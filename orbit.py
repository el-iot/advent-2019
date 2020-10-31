import collections
import json

with open("orbit_data.json", "r") as file:
    data = json.load(file)

pts, vel = data["points"], data["velocities"]


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def _lcm(x, y):
    lcm = (x * y) // gcd(x, y)
    return lcm


def lcm(x: list):
    if len(x) == 2:
        return _lcm(*x)
    return lcm([_lcm(*x[:2]), x[2:]])


def find_periodicity(sequence, min_points):
    pattern = sequence[:min_points]

    for idx in range(1, len(sequence)):
        if sequence[idx : idx + min_points] == pattern:
            return idx


periodicities = [
    find_periodicity(list(pts[f"{k1}"][k2]), 5)
    for k1 in [0, 1, 2, 3]
    for k2 in ["x", "y", "z"]
] + [
    find_periodicity(list(vel[f"{k1}"][k2]), 5)
    for k1 in [0, 1, 2, 3]
    for k2 in ["x", "y", "z"]
]

print(lcm(list(set(periodicities))))
