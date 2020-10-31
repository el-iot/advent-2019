from time import sleep

with open("map.txt", "r") as file:
    lines = [x for x in file.read().split("\n") if x]

# construct grid
grid = [[*line] for line in lines]


def render_grid(grid):
    """
    Render the grid
    """
    print(
        "\n".join(
            "".join(str(grid[y][x]) for x in range(len(grid[0])))
            for y in range(len(grid))
        )
    )
    print()


def get_neighbours(x, y):

    return [
        (x + i, y + j)
        for i, j in [(0, 1), (1, 0), (-1, 0), (0, -1)]
        if grid[y + j][x + i] == " "
    ]


filled = [(37, 37)]
time = 0

while " " in [i for j in grid for i in j]:

    new = []

    for x, y in filled:
        for xx, yy in get_neighbours(x, y):
            new.append((xx, yy))

    for x, y in new:
        filled.append((x, y))
        grid[y][x] = "O"

    time += 1
    sleep(0.01)
    render_grid(grid)
    filled = list(set(filled))

print(time)
