import json
import getopt
from generated.branch_pb2 import EventList, Interface
import os


def load_config_file():
    config: dict
    with open("./resources/config.json") as f:
        config = json.load(f)

    return config


def parse_cli_args(sys) -> dict:
    argument_list: list[str] = sys.argv[1:]
    options: str = "hi:o:"
    long_options: list = ["help", "input_file=", "output_folder="]

    input_file: str = ""
    output_folder: str = ""
    try:
        args, _ = getopt.getopt(argument_list, options, long_options)

        for arg, val in args:
            if arg in ("-h", "--help"):
                if sys.argv[0].endswith("run_branch.py"):
                    print(f"Usage: python ./{sys.argv[0]} -i /path/to/input.json")
                else:
                    print(f"Usage: python ./{sys.argv[0]} -i /path/to/input.json -o /path/to/output/folder")
                sys.exit()

            if arg in ("-i", "--input_file"):
                input_file = val

            if arg in ("-o", "--output_folder"):
                output_folder = os.path.abspath(val)

    except getopt.error as err:
        print("Error parsing input arguments:\n", err)

    if input_file == "":
        print("Input file must be given as argument. Use -h arg for usage details")
        sys.exit()

    if sys.argv[0].endswith("run_customer.py") and not output_folder:
        print("Output folder must be given as argument using -o|--output_folder")
        sys.exit()

    return {"input_file": input_file, "output_folder": output_folder}


def write_events(client_events: list[EventList], file_path: str):
    print_list = []
    for client_event in client_events:
        client = {
            "id": client_event.id,
            "type": client_event.type,
            "events": [{
                "customer-request-id": event.customer_request_id,
                "logical_clock": event.logical_clock,
                "interface": str(Interface.Name(event.interface)).lower(),
                "comment": event.comment
            } for event in client_event.events]
        }

        print_list.append(client)

    with open(file_path, 'w') as f:
        json.dump(print_list, f, indent=2)
