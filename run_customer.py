import json
import sys
import time

from services import Customer
from utils import parse_cli_args

program_args = parse_cli_args(sys)
input_json: list[dict]
with open(program_args["input_file"]) as f:
    input_json = json.load(f)

customer_events: list[dict] = list(filter(lambda x: x["type"] == "customer", input_json))
num_branches = len(list(filter(lambda x: x["type"] == "branch", input_json)))


# Sleep for 3 seconds just in case all thr branch servers haven't been started yet
time.sleep(3)

print_list = None
print("Executing customer events")

for customer_event in customer_events:
    customer = Customer(customer_event["id"], customer_event["events"], num_branches)
    print_list = customer.execute_events()

with open(program_args["output_file"], "w") as f:
    json.dump(print_list, f)

print(f"Output written to file: {program_args['output_file']}")
