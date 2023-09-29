import getopt
import sys
import json
from services import Customer

argument_list: list[str] = sys.argv[1:]
options: str = "hi:"
long_options: list = ["help", "input_file="]

input_file: str = ""

try:
    args, _ = getopt.getopt(argument_list, options, long_options)

    for arg, val in args:
        if arg in ("-h", "--help"):
            print("Usage: python ./run_customer.py -i /path/to/input.json")
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

customer_events: list[dict] = list(filter(lambda x: x["type"] == "customer", input_json))
start_port = config["start_port"]
customer_ids: set = set([customer_event["id"] for customer_event in customer_events])
customers: dict[Customer] = {}
for customer_id in customer_ids:
    customers[customer_id] = Customer(customer_id, start_port + customer_id)

for customer_event in customer_events:
    customers[customer_event["id"]].execute_events(customer_event["events"])

for customer_id in sorted(list(customers.keys())):
    customers[customer_id].print_events()
