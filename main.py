import sys
from typing import List
from timeit import timeit

from argument_processing import parse_arguments, validate_arguments
from data_generation import generate_data

random_data = ""

def test_generation(args):
   global random_data
   random_data = generate_data(args)

def main(argv: List[str]) -> int:
    try:
        parsed_args = parse_arguments(argv[1:])
        validate_arguments(parsed_args)
    except Exception as e:
        print(e)
        return -1

    if parsed_args.timeit:
        time = timeit(lambda: test_generation(parsed_args), number = 1, globals=globals())
        print("Execution time: " + str(time) + "\n")
    else:
       test_generation(parsed_args)

    # Q: не уверен, нужно ли замерять время вывода, вроде нет
    if parsed_args.output_path is not None:
        output_stream = open(parsed_args.output_path, "w")
    else:
        output_stream = sys.stdout

    output_stream.write(random_data)

    if parsed_args.output_path is not None:
        output_stream.close()

    return 0


if __name__=="__main__":
    main(sys.argv)