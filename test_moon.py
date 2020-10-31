import json

import moon

def test_moon():

    for config, step, expected in [
        (
            """<x=-1, y=0, z=2>\n<x=2, y=-10, z=-7>\n<x=4, y=-8, z=8>\n<x=3, y=5, z=-1>""",
            10,
            179,
        ),
        (
            """<x=-8, y=-10, z=0>\n<x=5, y=5, z=10>\n<x=2, y=-7, z=3>\n<x=9, y=-8, z=-3>""",
            100,
            1940,
        ),
    ]:
        planet = moon.Planet.from_string(config)
        for _ in range(step):
            planet.step()
        assert planet.energy() == expected
