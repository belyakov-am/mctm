from argparse import ArgumentParser
from collections import defaultdict
from decimal import getcontext, Decimal
from typing import Dict, Tuple, IO

# Constants
COMPRESS = 'compress'
DECOMPRESS = 'decompress'

PRECISION = 1000

# Type definitions
FrequencyTable = Dict[str, int]
ProbabilityTable = Dict[str, Decimal]
StepProbabilities = Dict[str, Tuple[Decimal, Decimal]]


def write_probs_to_file(probs: FrequencyTable, file: IO) -> None:
    total_items = len(probs.values())
    count = 0

    for k, v in probs.items():
        file.write(f'{k}:{v}')
        if count != total_items - 1:
            file.write(',')


class ArithmeticCoding:
    """
    Class for compressing and decompressing text from file using arithmetic coding method.

    Usage is pretty easy: just call compress for compressing and decompress for decompressing!
    """

    def __init__(self) -> None:
        self.freq_table: FrequencyTable = defaultdict(int)
        self.prob_table: ProbabilityTable = dict()
        self.text_size = 0

    def compress(self, input_name: str, output_name: str) -> None:
        """
        Compress text from input file to output.

        :param input_name: input file name with text
        :param output_name: output file name for compressed text
        """

        self._generate_prob_table(input_name)

        low = Decimal(0.0)
        high = Decimal(1.0)

        with open(input_name, 'r') as f:
            for line in f:
                for ch in line:
                    probs = self._step(self.prob_table, low, high)

                    low = probs[ch][0]
                    high = probs[ch][1]

            probs = self._step(self.prob_table, low, high)

        encoded_value = str(self._generate_encoded_value(probs))

        with open(output_name, 'w') as f:
            f.write(encoded_value + '\n')
            write_probs_to_file(self.freq_table, f)

    def decompress(self, input_name: str, output_name: str) -> None:
        """
        Decompress text from input file to output.

        :param input_name: input file name with compressed text
        :param output_name: output file name for decompressed text
        """

        self._read_freq_table(input_name)

        low = Decimal(0.0)
        high = Decimal(1.0)

        with open(input_name, 'r') as f:
            compressed_value = Decimal(f.readline())

        with open(output_name, 'w') as f:
            for _ in range(self.text_size):
                probs = self._step(self.prob_table, low, high)

                for ch, interval in probs.items():
                    if interval[0] <= compressed_value <= interval[1]:
                        break

                f.write(ch)

                low = interval[0]
                high = interval[1]

    def _fill_prob_table(self):
        for ch, count in self.freq_table.items():
            self.prob_table[ch] = Decimal(count / self.text_size)

    def _generate_prob_table(self, file_name: str) -> None:
        with open(file_name, 'r') as f:
            for line in f:
                for ch in line:
                    self.freq_table[ch] += 1
                    self.text_size += 1

        self._fill_prob_table()

    def _read_freq_table(self, file_name: str) -> None:
        with open(file_name, 'r') as f:
            # skip first line with encoded text
            f.readline()

            # read frequency table
            probs = f.read().split(',')
            for prob in probs:
                # skip last emtpy string
                if not prob:
                    continue

                ch, value = prob.rsplit(':', maxsplit=1)
                self.freq_table[ch] = int(value)
                self.text_size += self.freq_table[ch]

            self._fill_prob_table()

    def _step(self, prob_table: ProbabilityTable, low: Decimal, high: Decimal) -> StepProbabilities:
        probs: StepProbabilities = dict()

        length = high - low
        global_low = low

        for ch, prob in prob_table.items():
            current_high = global_low + prob * length
            probs[ch] = (global_low, current_high)
            global_low = current_high

        return probs

    def _generate_encoded_value(self, probs: StepProbabilities) -> Decimal:
        ends = []

        for low, high in probs.values():
            ends.append(low)
            ends.append(high)

        low = min(ends)
        high = max(ends)

        return (low + high) / 2


def init_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('option', nargs=1, choices=[COMPRESS, DECOMPRESS],
                        help='Option for either compressing or decompressing input file')
    parser.add_argument('input', nargs=1, help='Name of the input file')
    parser.add_argument('output', nargs=1, help='Name of the output file')
    parser.add_argument('--precision', type=int, default=PRECISION,
                        help='Number of decimal places for controlling algorithms quality')

    return parser


def main():
    parser = init_arg_parser()
    args = parser.parse_args()

    option = args.option[0]
    input_name = args.input[0]
    output_name = args.output[0]
    precision = args.precision

    # TODO: remove (?)
    getcontext().prec = precision

    coder = ArithmeticCoding()

    if option == COMPRESS:
        coder.compress(input_name, output_name)
    elif option == DECOMPRESS:
        coder.decompress(input_name, output_name)


if __name__ == '__main__':
    main()
