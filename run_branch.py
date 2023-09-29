import getopt
import sys
import json
from services import Branch

argument_list: list[str] = sys.argv[1:]
options: str = "hi:"
long_options: list = ["help", "input_file="]

input_file: str = ""
try:
    args, _ = getopt.getopt(argument_list, options, long_options)

    for arg, val in args:
        if arg in ("-h", "--help"):
            print("Usage: python ./run_branch.py -i /path/to/input.json"
                  "--input_file=/path/to/input.json")
            sys.exit()

        if arg in ("-i", "--input_file"):
            input_file = val

except getopt.error as err:
    print("Error parsing input arguments:\n", err)

if input_file == "":
    print("Input file must be given as argument. Use -h arg for usage details")
    sys.exit()

input_json: list[dict]
with open(input_file) as f:
    input_json = json.load(f)

config: dict
with open("./resources/config.json") as f:
    config = json.load(f)

branch_events: list[dict] = list(filter(lambda x: x["type"] == "branch", input_json))

start_port = config["start_port"]
branches: dict = {}
# We are adding port number to the branch info, which will be used as process_id for the branch
for branch_event in branch_events:
    branch = {**branch_event, "port": start_port + branch_event["id"]}
    branches[branch_event["id"]] = branch

servers = []

for branch in branches.values():
    port = start_port + branch["id"]
    servers.append(Branch.serve(branch["id"], branch["balance"], branches, port))

for server in servers:
    server.wait_for_termination()
