from tunnels import Solution


def test1():

    cases = [
        ("#########\n#b.A.@.a#\n#########", 8),
        (
            "########################\n#f.D.E.e.C.b.A.@.a.B.c.#\n######################.#\n#d.....................#\n########################",
            86,
        ),
    ]

    for i, o in cases:
        solution = Solution(i)
        paths = solution.traverse()
        assert min(paths)[0] == o
