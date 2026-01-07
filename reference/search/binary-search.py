import argparse
#<START>
def searcher(arr, low, high):
    #...
    print("tempo")

def search(numbers: list[int]):
    n = len(numbers)
    searcher(numbers, 0, n - 1)
    print(numbers)
#<STOP>
def parse_int_list(value):
    try:
        return [int(x) for x in value.split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Numbers must be a comma-separated list of integers"
        )

parser = argparse.ArgumentParser()
parser.add_argument(
    "numbers",
    type=parse_int_list,
    help="Comma-separated list of integers (e.g. 1,2,3)"
)

args = parser.parse_args()

search(args.numbers)
