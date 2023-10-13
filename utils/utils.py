import json
import getopt


def load_config_file():
    config: dict
    with open("./resources/config.json") as f:
        config = json.load(f)

    return config


def parse_cli_args(sys) -> dict:
    argument_list: list[str] = sys.argv[1:]
    options: str = "hi:"
    long_options: list = ["help", "input_file="]

    input_file: str = ""
    try:
        args, _ = getopt.getopt(argument_list, options, long_options)

        for arg, val in args:
            if arg in ("-h", "--help"):
                print(f"Usage: python ./{sys.argv[0]} -i /path/to/input.json")
                sys.exit()

            if arg in ("-i", "--input_file"):
                input_file = val

    except getopt.error as err:
        print("Error parsing input arguments:\n", err)

    if input_file == "":
        print("Input file must be given as argument. Use -h arg for usage details")
        sys.exit()

    return {"input_file": input_file}
