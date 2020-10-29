import json
import tqdm
import re

MOON_RE = re.compile(r"^\s*<x=(.*), y=(.*), z=(.*)>")


class Vector:
    """
    Vector for easy adding and subtracting
    """

    def __init__(self, *args):
        self.n = len(args)
        self.values = args

    def __add__(self, other):
        """
        Add vectors
        """

        assert self.n == other.n, "vectors must have the same length (%s != %s)" % (
            self.n,
            other.n,
        )
        result = [self.values[idx] + other.values[idx] for idx in range(self.n)]
        return Vector(*result)

    def __sub__(self, other):
        """
        Subtract vectors
        """

        assert self.n == other.n, "vectors must have the same length (%s != %s)" % (
            self.n,
            other.n,
        )
        result = [self.values[idx] - other.values[idx] for idx in range(self.n)]
        return Vector(*result)

    def __mul__(self, n):
        """
        Multiply vectors by a scalar
        """
        return Vector(*[x * n for x in self.values])

    def to_unit(self):
        """
        Get the unit vector
        """
        return Vector(*[1 if x > 0 else 0 if x == 0 else -1 for x in self.values])

    def __repr__(self):

        return f"<< {'-'.join(str(e) for e in self.values)} >>"


class Moon:
    def __init__(self, x, y, z):
        self.position = Vector(x, y, z)
        self.velocity = Vector(0, 0, 0)

    def energy(self):
        """
        Get the potential and kinetic energy of the moon
        """
        return self.potential_energy() * self.kinetic_energy()

    def potential_energy(self):
        return sum([abs(e) for e in self.position.values])

    def kinetic_energy(self):
        return sum([abs(e) for e in self.velocity.values])

    def __repr__(self):

        pad = lambda s: " " * (6 - len(str(s))) + str(s)

        return (
            f"pos ({', '.join(pad(e) for e in self.position.values)}) "
            f"vel ({', '.join(pad(e) for e in self.velocity.values)}) "
            f"en  ({', '.join(pad(e) for e in [self.kinetic_energy(), self.potential_energy(), self.energy()])})"
        )


class Planet:
    """
    Simulate the motion of the moons in time steps.
    """

    def __init__(self, moons):
        self.moons = moons

    def apply_gravity(self):

        for i, m1 in enumerate(self.moons):
            for j, m2 in enumerate(self.moons):

                if i >= j:
                    continue

                delta = (m2.position - m1.position).to_unit()

                m1.velocity += delta
                m2.velocity += delta * (-1)

    def apply_velocity(self):

        for moon in self.moons:
            moon.position += moon.velocity

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    def energy(self):
        return sum([moon.energy() for moon in self.moons])

    def kinetic_energy(self):
        return sum([moon.kinetic_energy() for moon in self.moons])

    def potential_energy(self):
        return sum([moon.potential_energy() for moon in self.moons])

    def display(self):

        for moon in self.moons:
            print(moon)

        print()

    def serialise(self):
        return tuple(
            [
                i
                for j in [
                    list(moon.position.values) + list(moon.velocity.values)
                    for moon in self.moons
                ]
                for i in j
            ]
        )

    @staticmethod
    def from_string(string):

        moons = [
            Moon(*[int(x) for x in MOON_RE.match(line).groups()])
            for line in string.split("\n")
        ]

        return Planet(moons)


if __name__ == "__main__":

    inputs = """<x=-4, y=-9, z=-3>
    <x=-13, y=-11, z=0>
    <x=-17, y=-7, z=15>
    <x=-16, y=4, z=2>"""

    jupyter = Planet.from_string(inputs)
    points = {key: {"x": [], "y": [], "z": []} for key in range(4)}
    velocities = {key: {"x": [], "y": [], "z": []} for key in range(4)}
    EPOCHS = 1000000

    for step in tqdm.tqdm(range(EPOCHS)):
        jupyter.step()
        for idx, moon in enumerate(jupyter.moons):
            [x, y, z] = moon.position.values
            points[idx]["x"].append(x)
            points[idx]["y"].append(y)
            points[idx]["z"].append(z)

            [x, y, z] = moon.velocity.values
            velocities[idx]["x"].append(x)
            velocities[idx]["y"].append(y)
            velocities[idx]["z"].append(z)

    with open("orbit_data.json", "w") as file:
        json.dump({"points": points, "velocities": velocities}, file)
