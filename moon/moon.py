import json
import re

import tqdm

MOON_RE = re.compile(r"^\s*<x=(.*), y=(.*), z=(.*)>")


class Vector:
    """
    Vector for easy adding and subtracting
    """

    def __init__(self, *args):
        self.n = len(args)
        self.values = args

    def __add__(self, other):

        assert self.n == other.n, "vectors must have the same length (%s != %s)" % (
            self.n,
            other.n,
        )
        result = [self.values[idx] + other.values[idx] for idx in range(self.n)]
        return Vector(*result)

    def __sub__(self, other):

        assert self.n == other.n, "vectors must have the same length (%s != %s)" % (
            self.n,
            other.n,
        )
        result = [self.values[idx] - other.values[idx] for idx in range(self.n)]
        return Vector(*result)

    def __mul__(self, n):
        return Vector(*[x * n for x in self.values])

    def to_unit(self):
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

        return (
            f"<< {' | '.join(str(e) for e in self.position.values)} >> "
            f"<< {' | '.join(str(e) for e in self.velocity.values)} >>"
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

    inputs = """pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
    pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>"""

    jupyter = Planet.from_string(inputs)

    kinetic_energies = []
    potential_energies = []
    energies = []
    moon_energies = [
        {
            "kinetic": [],
            "potential": [],
            "total": [],
        }
        for _ in range(len(jupyter.moons))
    ]

    for n in tqdm.tqdm(range(2772 * 4)):

        kinetic_energies.append(jupyter.kinetic_energy())
        potential_energies.append(jupyter.potential_energy())
        energies.append(jupyter.energy())

        for idx, moon in enumerate(jupyter.moons):

            moon_energies[idx]["kinetic"].append(moon.kinetic_energy())
            moon_energies[idx]["potential"].append(moon.potential_energy())
            moon_energies[idx]["total"].append(moon.energy())

        jupyter.step()

    with open("energy.json", "w") as file:
        json.dump(
            {
                "kinetic": kinetic_energies,
                "potential": potential_energies,
                "total": energies,
                "moons": moon_energies,
            },
            file,
        )
