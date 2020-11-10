import math

import numpy


def pt1(digits):

    signal = [int(x) for x in digits]
    signal_length = len(signal)
    base_pattern = [0, 1, 0, -1]

    def extend(x):
        return (x * math.ceil((signal_length + 1) / len(x)))[1 : signal_length + 1]

    def mutate(signal):
        values = numpy.array([signal for _ in range(signal_length)])
        result = numpy.abs(numpy.multiply(grid, values).sum(axis=1)) % 10
        return list(result)

    grid = numpy.array(
        [
            extend(sum([[element] * i for element in base_pattern], []))
            for i in range(1, signal_length + 1)
        ]
    )
    for i in range(100):
        signal = mutate(signal)

    print(signal)


def pt2(signal):
    """
    03036732577212944063491565474664 becomes 84462026

    Once you are 91% through the signal (as we are) we can actually forget about the
    front-end of the signal -> it's all just + from this point. This is a powerful thing.

    We just need to track how the signal-tail sum changes - everything else is figured out.

    Steps:
        Find the sliver of the signal that you are actually interested in -> the offset to the offset + 8.
        Calculate the sum of the signal after the sliver and take it modulo 10.
            For each element in the signal, use the signal-tail-sum and the old digit to determine the new digit.
            Recalculate the sum of the signal-tail.
            Repeat
    """
    offset = int(signal[:7])
    signal = [int(x) for x in signal]
    original_signal_length = len(signal)
    complete_signal_length = original_signal_length * 1e5

    print(offset / complete_signal_length)
    not_skipped = complete_signal_length - offset

    # first truncate the signal to only be the last 9% or so -> the digits in front do not matter
    quotient, remainder = divmod(offset, original_signal_length)
    piece = (signal * 2)[remainder : remainder + 8]

    # we have to construct the tail of the signal
    signal_tail = (signal * 2)[remainder + 8 :] + signal * (
        int(not_skipped // len(signal)) - 1
    )

    print(f"SIGNAL TAIL IS {len(signal_tail)} LONG")
    print(len(signal_tail) + offset + 8)
    print(len(signal))
    # now find the sum of the signal and how many times it has been applied
    signal_sum = sum(signal)
    # each element has the `signal_sum` added `quotient` times before we consider the tail
    signal_tail_sum = signal_sum * quotient

    for _ in range(100):
        # update signal tail sum and relevant section
        pass


if __name__ == "__main__":

    pt1("12345")
    pt1("1234512345")
