import sys
import json
from services import Branch
from utils import parse_cli_args, load_config_file

program_args = parse_cli_args(sys)
input_json: list[dict]
with open(program_args["input_file"]) as f:
    input_json = json.load(f)

config = load_config_file()
start_port = config["start_port"]

branch_events: list[dict] = list(filter(lambda x: x["type"] == "branch", input_json))
branch_ids = [start_port + branch_event["id"] for branch_event in branch_events]

servers = []
for branch_event in branch_events:
    branch = Branch(branch_event["id"], branch_event["balance"], branch_ids)
    servers.append(branch.serve())

for server in servers:
    server.wait_for_termination()
