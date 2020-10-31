import math
"""
Each element in the new list is built by multiplying every value in the input list by a value in a repeating pattern and then adding up the results. So, if the input list were 9, 8, 7, 6, 5 and the pattern for a given element were 1, 2, 3, the result would be 9*1 + 8*2 + 7*3 + 6*1 + 5*2 (with each input element on the left and each value in the repeating pattern on the right of each multiplication). Then, only the ones digit is kept: 38 becomes 8, -17 becomes 7, and so on.

While each element in the output array uses all of the same input array elements, the actual repeating pattern to use depends on which output element is being calculated. The base pattern is 0, 1, 0, -1. Then, repeat each value in the pattern a number of times equal to the position in the output list being considered. Repeat once for the first element, twice for the second element, three times for the third element, and so on. So, if the third element of the output list is being calculated, repeating the values would produce: 0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1.

When applying the pattern, skip the very first value exactly once. (In other words, offset the whole pattern left by one.) So, for the second element of the output list, the actual pattern used would be: 0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1, ....

After using this process to calculate each element of the output list, the phase is complete, and the output list of this phase is used as the new input list for the next phase, if any.
"""


def next_phase(signal):

    output = []
    for i, digit in enumerate(signal):
        pattern = [
            i
            for j in [[element for _ in range(i + 1)] for element in base_pattern]
            * math.ceil(len(signal) // (4 * 2 ** (i + 1)) + 0.01)
            for i in j
        ][i:]
        result = sum([x * y for x, y in zip(signal, pattern)])
        output.append(abs(result) % 10)

    return output


base_pattern = [0, 1, 0, -1]
signal = [int(x) for x in "12345678"]

for i in range(10):
    print(signal)
    signal = next_phase(signal)

print(signal)
