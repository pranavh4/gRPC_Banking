import json

import grpc
from generated.branch_pb2_grpc import BranchStub
from generated.branch_pb2 import *
from utils import load_config_file

config = load_config_file()
start_port = config["start_port"]


class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recv_msg: list[Response] = list()
        # pointer for the stub
        self.stub = self.create_stub()

    def create_stub(self) -> BranchStub:
        channel = grpc.insecure_channel(f'localhost:{start_port + self.id}')
        return BranchStub(channel)

    def execute_events(self):
        for event in self.events:
            if event["interface"] == "query":
                request = Request(interface=Interface.Query, id=self.id)
            elif event["interface"] == "deposit":
                request = Request(interface=Interface.Deposit, id=self.id, money=event["money"])
            elif event["interface"] == "withdraw":
                request = Request(interface=Interface.Withdraw, id=self.id, money=event["money"])
            else:
                raise Exception("Invalid Event Type")

            self.recv_msg.append(self.stub.MsgDelivery(request))

        self.print_events()

    def print_events(self):
        print_dict = {"id": self.id, "recv": []}
        for msg in self.recv_msg:
            if msg.interface == Interface.Query:
                print_dict["recv"].append({"interface": "query", "balance": msg.money})
            else:
                print_dict["recv"].append({
                    "interface": Interface.Name(msg.interface).lower(),
                    "result": ResponseStatus.Name(msg.status).lower()
                })

        print(json.dumps(print_dict))
