import argparse
#<START>
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def sorter(arr, low, high):
    if low >= high or low < 0:
        return
    
    p = partition(arr, low, high)
    sorter(arr, low, p - 1)
    sorter(arr, p + 1, high)

def sort(numbers: list[int]):
    n = len(numbers)
    sorter(numbers, 0, n - 1)
    print(",".join(map(str, numbers)))
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

sort(args.numbers)
