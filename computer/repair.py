import json

from computer import Computer

HEIGHT = 50
WIDTH = 50


class Tiles:

    START = -2
    UNKNOWN = -1
    SPACE = 0
    WALL = 1
    OXYGEN = 2
    DROID = 3
    CHARACTERS = {UNKNOWN: ".", SPACE: " ", WALL: "▒", OXYGEN: "O", START: "X"}


class Directions:

    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    MOVES = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}


class Responses:

    HIT_WALL = 0
    MOVED = 1
    FOUND_OXYGEN = 2


class RepairDroid(Computer):
    """
    Repair droid
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.width = WIDTH
        self.height = HEIGHT
        self.grid = [[-1 for _ in range(WIDTH)] for _ in range(HEIGHT)]

        self.x = self.width // 2
        self.y = self.height // 2
        self.start = (self.x, self.y)

        self.path = []
        self.seen = {}
        self.step = 0

    def get_inputs(self):
        """
        Get the inputs - work out which direction to move in next
        """
        preferences = ["NORTH", "WEST", "SOUTH", "EAST"]
        bias = ["NORTH", "WEST", "SOUTH", "EAST"]

        def get_preference(direction):

            # 3 keys: (valid, new, time since visiting (-1 for new))

            ident = getattr(Directions, direction)
            dx, dy = Directions.MOVES[ident]
            new_x, new_y = self.x + dx, self.y + dy

            assert 0 <= new_x < self.width
            assert 0 <= new_y < self.height

            valid = (
                # HACK HERE
                (new_x, new_y) != (37, 37)
                and 0 <= new_x < self.width
                and 0 <= new_y < self.height
                and self.grid[new_y][new_x] != Tiles.WALL
            )

            if not valid:
                return (valid, -1, -1, -1)

            new = self.grid[new_y][new_x] not in self.seen

            return valid, new, -self.seen.get((new_x, new_y), -1), bias.index(direction)

        sorted_preferences = sorted(preferences, key=get_preference, reverse=True)

        for preference in sorted_preferences:

            ident = getattr(Directions, preference)
            dx, dy = Directions.MOVES[ident]
            self.desired_x = self.x + dx
            self.desired_y = self.y + dy
            return [ident]

        raise ValueError("trapped?")

    def process_outputs(self, output):
        """
        Process the outputs
        """

        if output == Responses.HIT_WALL:
            self.grid[self.desired_y][self.desired_x] = Tiles.WALL

        elif output == Responses.MOVED:
            self.path.append((self.x, self.y))
            self.grid[self.desired_y][self.desired_x] = Tiles.SPACE
            self.seen[(self.x, self.y)] = self.step
            self.step += 1
            self.x, self.y = self.desired_x, self.desired_y

        elif output == Responses.FOUND_OXYGEN:
            self.path.append((self.x, self.y))
            self.path.append((self.desired_x, self.desired_y))
            self.grid[self.desired_y][self.desired_x] = Tiles.OXYGEN
            self.finished = True
        else:
            raise ValueError("unknown response: %s" % output)

        self.desired_x = None
        self.desired_y = None

        self.render_grid()

    def render_grid(self):
        """
        Render the grid
        """
        print(
            "\n".join(
                "".join(
                    Tiles.CHARACTERS[self.grid[y][x]]
                    if (x, y) != (self.x, self.y)
                    else "+"
                    for x in range(self.width)
                )
                for y in range(self.height)
            )
        )
        print()

    def run(self):
        """
        Run the program
        """
        self.inputs = self.get_inputs()

        while not self.finished:
            instructions = self.read_next_instruction()
            output = self.execute(**instructions)
            if output is not None:
                self.process_outputs(output)

        return len(self.truncate_path()) - 1

    def truncate_path(self):
        """
        Truncate the path
        """
        path = self.path.copy()
        output = []
        idx = 0

        while idx < len(path):
            x, y = path[idx]
            if path[idx:].count((x, y)) > 1:
                last_index = len(path) - path[::-1].index((x, y)) - 1
                idx = last_index + 1
            else:
                idx += 1
            output.append((x, y))
        return output


if __name__ == "__main__":

    with open("repair_program.json", "r") as file:
        program = json.load(file)

    droid = RepairDroid(program)
    path = droid.run()
    print(path)
