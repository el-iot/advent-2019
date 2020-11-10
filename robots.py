import collections


class Tiles:
    SPACE = "."
    WALL = "#"
    KEYS = "abcdefghijklmnopqrstuvwxyz"
    DOORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ROBOTS = "1234"


class Tunnel:
    def __init__(self, input_string):

        self.grid = [[*row] for row in input_string.split("\n") if row]

        self.height = len(self.grid)
        self.width = len(self.grid[0])

        n_players = input_string.count("@")

        if n_players not in [1, 4]:
            raise ValueError("bad number of players (%s)" % n_players)

        if n_players == 1:

            print("modifying centre")

            replacement_pattern = ["1#2", "###", "3#4"]

            x, y = [
                (x - 1, y - 1)
                for x in range(self.width)
                for y in range(self.height)
                if self.grid[y][x] == "@"
            ][0]

            for dx in range(3):
                for dy in range(3):
                    self.grid[y + dy][x + dx] = replacement_pattern[dy][dx]

        elif n_players == 4:

            replacements = [*"1234"]
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid[y][x] == "@":
                        self.grid[y][x] = replacements.pop(0)

        self.all_robots = []
        self.robot_positions = {}
        self.all_keys = []
        self.key_positions = {}

        for y in range(self.height):
            for x in range(self.width):

                tile = self.grid[y][x]
                if tile in Tiles.ROBOTS:
                    self.robot_positions[tile] = (x, y)
                    self.all_robots.append(tile)

                elif tile in Tiles.KEYS:
                    self.key_positions[tile] = (x, y)
                    self.all_keys.append(tile)

        self.key_allocations = {
            robot: self.get_key_allocations(robot) for robot in self.all_robots
        }

        self.key_distances = self.get_key_distances()

        self.render_grid()

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

    def solve(self):
        """
        Find the minimum number of steps to solve the puzzle
        """

        robot_positions = [v for k, v in sorted(self.robot_positions.items())]
        minimum_distance = float("inf")
        queue = [(robot_positions, [], 0)]
        best = {}

        while queue:

            positions, found_keys, total_distance = queue.pop(0)

            _id = (
                (tuple(position) for position in positions),
                "".join(sorted(found_keys)),
            )

            if best.get(_id, float("inf")) <= total_distance:
                continue

            best[_id] = total_distance

            if total_distance >= minimum_distance:
                continue

            if len(found_keys) == len(self.all_keys):
                minimum_distance = min(minimum_distance, total_distance)
                print(minimum_distance)
                continue

            for idx, (robot, position) in enumerate(zip(self.all_robots, positions)):
                robot_tile = self.grid[position[1]][position[0]]
                for next_key in sorted(
                    self.key_allocations[robot],
                    key=lambda k: self.key_distances[robot_tile][k],
                    reverse=True,
                ):
                    if next_key not in found_keys and all(
                        req in found_keys
                        for req in self.key_allocations[robot][next_key]
                    ):
                        distance = self.key_distances[robot_tile][next_key]
                        queue.insert(
                            0,
                            (
                                positions[:idx]
                                + [self.key_positions[next_key]]
                                + positions[idx + 1 :],
                                found_keys + [next_key],
                                total_distance + distance,
                            ),
                        )

        return minimum_distance

    def get_key_distances(self):
        """
        Get the inter-key distances
        """
        return {
            key: self._get_key_distances(key)
            for key in self.all_keys + [*self.robot_positions]
        }

    def _get_key_distances(self, key):
        """
        Helper function
        """
        x, y = self.key_positions.get(key, self.robot_positions.get(key))

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

    def get_key_allocations(self, robot):
        """
        Get the keys that belong to each robot, and evaluate which
        doors are needed to unlock to reach each key
        """
        requirements = collections.defaultdict(list)
        x, y = self.robot_positions[robot]
        seen = {*()}

        queue = [(x, y, [])]

        while queue:

            x, y, required = queue.pop(0)

            if (x, y) in seen:
                continue

            seen |= {(x, y)}

            tile = self.grid[y][x]

            if tile in Tiles.DOORS:
                required = required + [tile.lower()]

            elif tile in Tiles.KEYS:
                requirements[tile].append(required)

            elif tile in Tiles.WALL:
                continue

            for xx, yy in self.get_neighbours(x, y):
                queue.append((xx, yy, required))

        requirements = {
            key: [v for v in value[0] if all(v in vv for vv in value)]
            for key, value in requirements.items()
        }

        return requirements


"""
        1: {
                'a': ["B"],
                'c': ["E", "F"]
                'd': []
            }
"""
if __name__ == "__main__":

    import requests

    url = "https://adventofcode.com/2019/day/18/input"
    cookies = {
        "session": "53616c7465645f5f8dd5ab6cc0437ff5bc9ab097b3c098ca1f39fb037f87f7fb55feea5b92f65b11b1ba3842526a2cd7"
    }
    puzzle_input = requests.get(url, cookies=cookies).text
    tunnel = Tunnel(puzzle_input)
    d = tunnel.solve()
    print(d)
