import math


def angle_between(x1, y1, x2, y2):
    return ((math.atan2(y2 - y1, x2 - x1) * 180 / math.pi) + 90) % 360


def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def laser(x, y, galaxy):

    height = len(galaxy)
    width = len(galaxy[0])
    asteroids = sorted(
        [
            (xx, yy, angle_between(x, y, xx, yy))
            for xx in range(width)
            for yy in range(height)
            if galaxy[yy][xx] == "#" and (xx, yy) != (x, y)
        ],
        key=lambda e: (e[2], distance_between(x, y, *e[:2])),
    )

    destroyed = []

    while asteroids:
        last_angle = None
        idx = 0

        while asteroids and idx < len(asteroids):

            [x, y, angle] = asteroids[idx]

            if angle == last_angle:
                idx += 1
                last_angle = angle
                continue

            last_angle = angle
            destroyed.append(asteroids.pop(idx))

    return destroyed


if __name__ == "__main__":

    with open("test1.txt", "r") as file:
        galaxy = [[*line] for line in file.read().split()]

    result = laser(11, 13, galaxy)
    print(result[199])
