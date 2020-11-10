import collections


class Tiles:
    SPACE = "."
    WALL = "#"
    KEYS = "abcdefghijklmnopqrstuvwxyz"
    DOORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    PLAYER = "@1234"


class Solution:
    def __init__(self, input_string):
        """
        Initialise
        """
        self.grid = [[*line] for line in input_string.split("\n") if line]

        self.height = len(self.grid)
        self.width = len(self.grid[0])

        # replace the existing pattern with a new one
        (x, y) = self._find_player()
        x -= 1
        y -= 1
        replacement_pattern = ["1#2", "###", "3#4"]

        self.robots = []

        for i in range(3):
            for j in range(3):
                self.grid[y + i][x + j] = replacement_pattern[j][i]
                if self.grid[y + i][x + j] in Tiles.PLAYER:
                    self.robots.append((x + j, y + i))

        self.render_grid()

        self.key_requirements = self.get_key_requirements()
        print(self.key_requirements)
        self.key_distances = self.get_key_distances()
        self.key_locations = {
            self.grid[y][x]: (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if self.grid[y][x] in Tiles.KEYS
        }

        self.all_keys = [i for j in self.grid for i in j if i in Tiles.KEYS]

    def render_grid(self):
        print("\n".join(["".join(str(key) for key in row) for row in self.grid]) + "\n")

    def get_neighbours(self, x, y):
        """
        Get neighbouring coordinates of x, y
        """
        return [
            (x + i, y + j)
            for i, j in [(0, 1), (1, 0), (0, -1), (-1, 0)]
            if 0 <= x + i < self.width and 0 <= y + j < self.height
        ]

    @staticmethod
    def has_keys(grid) -> bool:
        """
        Find whether there are currently any keys left in the tunnels
        """
        return any([i in Tiles.KEYS for j in grid for i in j])

    def _find_player(self) -> None:
        """
        Find the player in the grid and assign the x, y coordinate
        of the player on self
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x] == Tiles.PLAYER:
                    return x, y

    def unlock(self, grid, key):
        """
        Unlock the door corresponding to a given key
        """
        door = key.upper()
        for x in range(self.width):
            for y in range(self.height):
                if grid[y][x] == door:
                    grid[y][x] = Tiles.SPACE
                    return

    def traverse(self):
        """
        Collect the keys
        """
        solutions = []
        lowest_steps = float("inf")
        best = {}
        queue = [(*self.starting_coordinates, 0, [])]

        while queue:

            x, y, steps, unlocked = queue.pop(0)
            tile = self.grid[y][x]

            _id = (x, y, "".join(sorted(unlocked)))

            if best.get(_id, float("inf")) <= steps:
                continue

            best[_id] = steps

            if steps >= lowest_steps:
                continue

            if (key := self.grid[y][x]) in Tiles.KEYS:
                unlocked = unlocked + [key]

                if len(unlocked) == len(self.all_keys):
                    lowest_steps = min(lowest_steps, steps)
                    solutions.append((steps, unlocked))
                    continue

            available_keys = self.get_available_keys(tile, unlocked)

            for key in available_keys[::-1]:
                distance = self.key_distances[tile][key]
                queue.insert(0, (*self.key_locations[key], steps + distance, unlocked))

        return solutions

    def get_available_keys(self, tile, owned_keys):
        """
        Find any keys currently available to the player
        """
        candidates = [
            c
            for c in self.all_keys
            if c not in owned_keys
            and all(req.lower() in owned_keys for req in self.key_requirements[c])
        ]
        return sorted(candidates, key=lambda x: self.key_distances[tile][x])

    def get_key_requirements(self):
        """
        Get the key-requirements
        """
        requirements = collections.defaultdict(list)
        queue = [([], [])]
        seen = {*()}

        while queue:

            x, y, required = queue.pop(0)

            if (x, y) in seen:
                continue

            seen |= {(x, y)}
            tile = self.grid[y][x]

            if tile in Tiles.KEYS:
                requirements[tile].append(required)

            if tile in Tiles.WALL:
                continue

            if tile in Tiles.DOORS:
                required = required + [tile]

            for xx, yy in self.get_neighbours(x, y):
                queue.append((xx, yy, required))

        items = {key: sorted(value, key=len)[0] for key, value in requirements.items()}

        return items

    def get_key_distances(self):
        """
        Get the key-requirements
        """
        key_locations = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if self.grid[y][x] in Tiles.KEYS
        ] + [self.starting_coordinates]

        return {
            self.grid[y][x]: self._get_key_distances(x, y) for x, y in key_locations
        }

    def _get_key_distances(self, x, y):

        queue = [(x, y, 0)]
        seen = {*()}
        distances = collections.defaultdict(list)

        while queue:

            x, y, n = queue.pop(0)

            if (x, y) in seen:
                continue

            seen |= {(x, y)}

            tile = self.grid[y][x]

            if tile in Tiles.KEYS:
                distances[tile].append(n)

            if tile in Tiles.WALL:
                continue

            for xx, yy in self.get_neighbours(x, y):
                queue.append((xx, yy, n + 1))

        return {key: min(value) for key, value in distances.items()}


if __name__ == "__main__":

    import requests

    url = "https://adventofcode.com/2019/day/18/input"
    cookies = {
       "session": "53616c7465645f5f8dd5ab6cc0437ff5bc9ab097b3c098ca1f39fb037f87f7fb55feea5b92f65b11b1ba3842526a2cd7"
    }
    puzzle_input = requests.get(url, cookies=cookies).text
    solution = Solution(puzzle_input)
    paths = solution.traverse()
    print(paths[-1])
