import math


def get_visible_asteroids(x, y, locations) -> int:
    """
    Get the number of visible asteroids from a given point, (x, y)
    """
    asteroids = sorted(
        [a for a in locations if a != (x, y)],
        key=lambda a: math.sqrt((x - a[0]) ** 2 + (y - a[1]) ** 2),
    )
    visible = 0
    angles = {*()}

    for (xx, yy) in asteroids:

        angle = math.atan2(yy - y, xx - x)

        if angle not in angles:
            angles |= {angle}
            visible += 1

    return visible


def best_location(galaxy):
    """
    Find the location a given galaxy with the most visible asteroids
    """
    height = len(galaxy)
    width = len(galaxy[0])

    result = [["." for _ in range(width)] for _ in range(height)]
    locations = [
        (x, y) for x in range(width) for y in range(height) if galaxy[y][x] == "#"
    ]

    most_visible = 0
    coordinate = None

    for (x, y) in locations:
        visible = get_visible_asteroids(x, y, locations)
        if visible > most_visible:
            most_visible = visible
            coordinate = (x, y)
        result[y][x] = str(visible)

    max_length = len(str(most_visible))
    return coordinate, most_visible


if __name__ == "__main__":

    with open("test1.txt", "r") as file:
        galaxy = [[*line] for line in file.read().split()]

    print(best_location(galaxy))
