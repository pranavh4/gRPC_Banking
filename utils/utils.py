import json
import getopt
import os


def load_config_file():
    config: dict
    with open("./resources/config.json") as f:
        config = json.load(f)

    return config


def parse_cli_args(sys) -> dict:
    argument_list: list[str] = sys.argv[1:]
    options: str = "hi:o:"
    long_options: list = ["help", "input_file=", "output_file="]

    input_file: str = ""
    output_file: str = ""
    try:
        args, _ = getopt.getopt(argument_list, options, long_options)

        for arg, val in args:
            if arg in ("-h", "--help"):
                if sys.argv[0].endswith("run_branch.py"):
                    print(f"Usage: python ./{sys.argv[0]} -i /path/to/input.json")
                else:
                    print(f"Usage: python ./{sys.argv[0]} -i /path/to/input.json -o /path/to/output.json")
                sys.exit()

            if arg in ("-i", "--input_file"):
                input_file = val

            if arg in ("-o", "--output_file"):
                output_file = os.path.abspath(val)

    except getopt.error as err:
        print("Error parsing input arguments:\n", err)

    if input_file == "":
        print("Input file must be given as argument. Use -h arg for usage details")
        sys.exit()

    if sys.argv[0].endswith("run_customer.py") and not output_file:
        print("Output file must be given as argument using -o|--output_file")
        sys.exit()

    return {"input_file": input_file, "output_file": output_file}

