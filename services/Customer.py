import json

import grpc
from generated.branch_pb2_grpc import BranchStub
from generated.branch_pb2 import *
import time


class Customer:
    def __init__(self, id, port):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = list()
        # a list of received messages used for debugging purpose
        self.recv_msg = list()
        # pointer for the stub
        channel = grpc.insecure_channel(f'localhost:{port}')
        self.stub = BranchStub(channel)

    # TODO: students are expected to send out the events to the Bank
    def execute_events(self, events):
        self.events.extend(events)

        for event in events:
            if event["interface"] == "query":
                self.recv_msg.append(self.stub.Query(QueryRequest(customer_id=self.id)))
            elif event["interface"] == "deposit":
                self.recv_msg.append(self.stub.Deposit(TransactionRequest(customer_id=self.id, amount=event["money"])))
            elif event["interface"] == "withdraw":
                self.recv_msg.append(self.stub.Withdraw(TransactionRequest(customer_id=self.id, amount=event["money"])))
            else:
                raise Exception("Invalid Event Type")

            # time.sleep(3)

    def print_events(self):
        print_dict = {"id": self.id, "recv": []}
        for msg in self.recv_msg:
            if type(msg) is TransactionResponse:
                print_dict["recv"].append({"interface": msg.interface, "result": msg.result})
            elif type(msg) is Balance:
                print_dict["recv"].append({"interface": "query", "balance": msg.money})

        print(json.dumps(print_dict))

