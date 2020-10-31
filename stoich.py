import collections
import math
import re
import time

REACTION_RE = re.compile(r"(?P<inputs>.*) => (?P<outputs>.*)")


class Reaction:
    """
    Chemical reaction
    """

    def __init__(self, inputs, output_chemical, output_amount):

        self.inputs = inputs
        self.outputs = {output_chemical: output_amount}

    def __repr__(self):

        return (
            "("
            + " + ".join(f"{value} {key}" for key, value in self.inputs.items())
            + " = "
            + " + ".join(f"{value} {key}" for key, value in self.outputs.items())
            + ")"
        )


def get_orders(reactions):
    """
    Get the usage-order of each chemical
    """
    orders = collections.defaultdict(list)
    io = dict([[[*r.outputs][0], list(r.inputs)] for r in reactions])
    queue = [("FUEL", 0)]

    while queue:
        c1, order = queue.pop(0)
        orders[c1].append(order)
        for c2 in io.get(c1, []):
            queue.append((c2, order + 1))

    return {key: max(values) for key, values in orders.items()}


def parse_reactions(s: str) -> Reaction:
    """
    Parse the reactions in a given string
    """
    reactions = []

    for line in s.split("\n"):

        if not (match := REACTION_RE.match(line)):
            raise ValueError(f"couldn't match pattern: {line}")

        groups = match.groupdict()
        inputs = {
            c: int(q) for [q, c] in [x.split() for x in groups["inputs"].split(", ")]
        }
        output_amount, output_chemical = groups["outputs"].split(" ")
        reactions.append(Reaction(inputs, output_chemical, int(output_amount)))

    return reactions


def get_ore(reaction_string: str, fuel: int):
    """
    Get the required amount of ore to produce `fuel` fuel given a
    string of reactions, `reaction_string`
    """

    reactions = parse_reactions(reaction_string)
    required = collections.defaultdict(int, {"FUEL": fuel})
    excess = collections.defaultdict(int)
    order = get_orders(reactions)
    ore = 0

    while any(amount > 0 for amount in required.values()):

        required_chemical, required_quantity = sorted(
            [(key, value) for key, value in required.items() if value > 0],
            key=lambda x: order[x[0]],
        )[0]

        if required_chemical == "ORE":
            ore += required_quantity
            required["ORE"] = 0
            continue

        if (xs := excess[required_chemical]) > 0:

            applicable = min(xs, required_quantity)
            required_quantity -= applicable
            excess[required_chemical] -= applicable

            if not required_quantity:
                continue

        available_reactions = [
            rx for rx in reactions if required_chemical in rx.outputs
        ]

        reaction = available_reactions[0]

        n_reactions = math.ceil(required_quantity / reaction.outputs[required_chemical])
        amount_produced = n_reactions * reaction.outputs[required_chemical]
        excess[required_chemical] += amount_produced - required_quantity
        required[required_chemical] -= required_quantity

        for input_chemical in reaction.inputs:
            required[input_chemical] += n_reactions * reaction.inputs[input_chemical]

    return ore


if __name__ == "__main__":

    s = """1 JNDQ, 11 PHNC => 7 LBJSB
    1 BFKR => 9 VGJG
    11 VLXQL => 5 KSLFD
    117 ORE => 6 DMSLX
    2 VGJG, 23 MHQGW => 6 HLVR
    2 QBJLJ => 6 DBJZ
    1 CZDM, 21 ZVPJT, 1 HLVR => 5 VHGQP
    1 RVKX => 1 FKMQD
    38 PHNC, 10 MHQGW => 5 GMVJX
    4 CZDM, 26 ZVHX => 7 QBGQB
    5 LBJSB, 2 DFZRS => 4 QBJLJ
    4 TJXZM, 11 DWXW, 14 VHGQP => 9 ZBHXN
    20 VHGQP => 8 SLXQ
    1 VQKM => 9 BDZBN
    115 ORE => 4 BFKR
    1 VGJG, 1 SCSXF => 5 PHNC
    10 NXZXH, 7 ZFXP, 7 ZCBM, 7 MHNLM, 1 BDKZM, 3 VQKM => 5 RMZS
    147 ORE => 2 WHRD
    16 CQMKW, 8 BNJK => 5 MHNLM
    1 HLVR => 5 TJQDC
    9 GSLTP, 15 PHNC => 5 SFZTF
    2 MJCD, 2 RVKX, 4 TJXZM => 1 MTJSD
    1 DBJZ, 3 SLXQ, 1 GMSB => 9 MGXS
    1 WZFK => 8 XCMX
    1 DFZRS => 9 GSLTP
    17 PWGXR => 2 DFZRS
    4 BFKR => 7 JNDQ
    2 VKHN, 1 SFZTF, 2 PWGXR => 4 JDBS
    2 ZVPJT, 1 PHNC => 6 VQKM
    18 GMSB, 2 MGXS, 5 CQMKW => 3 XGPXN
    4 JWCH => 3 BNJK
    1 BFKR => 2 PWGXR
    12 PHNC => 2 GMSB
    5 XGPXN, 3 VQKM, 4 QBJLJ => 9 GXJBW
    4 MHQGW => 9 DWXW
    1 GMSB, 1 BFKR => 5 DBKC
    1 VLXQL, 10 KSLFD, 3 JWCH, 7 DBKC, 1 MTJSD, 2 WZFK => 9 GMZB
    4 JDBS => 8 BRNWZ
    2 ZBHXN => 7 HMNRT
    4 LBJSB => 7 BCXGX
    4 MTJSD, 1 SFZTF => 8 ZCBM
    12 BRNWZ, 4 TJXZM, 1 ZBHXN => 7 WZFK
    10 HLVR, 5 LBJSB, 1 VKHN => 9 TJXZM
    10 BRNWZ, 1 MTJSD => 6 CMKW
    7 ZWHT => 7 VKHN
    5 CQMKW, 2 DBKC => 6 ZFXP
    1 CMKW, 5 JNDQ, 12 FKMQD, 72 BXZP, 28 GMVJX, 15 BDZBN, 8 GMZB, 8 RMZS, 9 QRPQB, 7 ZVHX => 1 FUEL
    10 MGXS => 9 JWCH
    1 BFKR => 8 SCSXF
    4 SFZTF, 13 CZDM => 3 RVKX
    1 JDBS, 1 SFZTF => 9 TSWV
    2 GMVJX, 1 PHNC => 1 CZDM
    6 JDBS => 1 BXZP
    9 TSWV, 5 TJXZM => 8 NXZXH
    1 HMNRT, 5 TSWV => 4 VLXQL
    16 WZFK, 11 XCMX, 1 GXJBW, 16 NXZXH, 1 QBGQB, 1 ZCBM, 10 JWCH => 3 QRPQB
    12 SCSXF, 6 VGJG => 4 ZVPJT
    10 JNDQ => 3 ZWHT
    1 DBJZ, 9 BCXGX => 2 CQMKW
    1 WHRD, 14 DMSLX => 8 MHQGW
    3 VKHN, 8 TJQDC => 4 MJCD
    1 QBJLJ => 4 ZVHX
    1 MHQGW, 4 ZVHX => 3 BDKZM"""

    # it's a binary search, dummy
    left, right = 1e2, 5e7

    while True:

        middle = (left + right) // 2
        ore = get_ore(s, middle)
        print(middle, ore)
        if ore > 1e12:
            right = middle
        else:
            left = middle

        time.sleep(0.05)
