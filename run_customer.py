import json
import sys
import time
from utils import write_events, parse_cli_args

from services import Customer
from generated.branch_pb2 import Interface

program_args = parse_cli_args(sys)
input_json: list[dict]
with open(program_args["input_file"]) as f:
    input_json = json.load(f)

customers: list[dict] = list(filter(lambda x: x["type"] == "customer", input_json))

print("Sleeping for 3 seconds just in case all the branch servers haven't been started yet")
time.sleep(3)

print("Executing customer requests")
customer_events = []
customer_clients = []
for customer in customers:
    customer = Customer(customer["id"], customer["customer-requests"])
    customer.execute_customer_requests()
    customer_events.append(customer.get_customer_events())
    customer_clients.append(customer)

# Get all the branch events once all the customer requests are done
branch_events = []
for customer_client in customer_clients:
    branch_events.append(customer_client.get_branch_events())

output_file = f'{program_args["output_folder"]}/output1.json'
write_events(customer_events, output_file)
print(f"Part 1: List all the events taken place on each customer. Written to file: {output_file}")

output_file = f'{program_args["output_folder"]}/output2.json'
write_events(branch_events, output_file)
print(f"\nPart 2: List all the events taken place on each branch. Written to file: {output_file}")

sorted_events = []
for client_event in customer_events + branch_events:
    sorted_events += [{
        "id": client_event.id,
        "customer-request-id": event.customer_request_id,
        "type": client_event.type,
        "logical_clock": event.logical_clock,
        "interface": str(Interface.Name(event.interface)).lower(),
        "comment": event.comment
    } for event in client_event.events]

sorted_events = sorted(sorted_events, key=lambda x: (x["customer-request-id"], x["logical_clock"]))

output_file = f'{program_args["output_folder"]}/output3.json'
with open(output_file, 'w') as f:
    json.dump(sorted_events, f, indent=2)

print("\nPart 3: List all the events (along with their logical times)"
      f" triggered by each customer Deposit/Withdraw request. Written to file {output_file}")
