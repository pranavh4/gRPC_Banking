import json

import grpc
from generated.branch_pb2_grpc import BranchStub
from generated.branch_pb2 import *
from utils import load_config_file

config = load_config_file()
start_port = config["start_port"]


class Customer:
    def __init__(self, id, events, num_branches):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recv_msg: list[Response] = list()
        # pointers for the branch stubs
        self.stubs = [None] + [create_stub(i + 1) for i in range(num_branches)]
        # Indicates the last commit id return from a branch
        self.commit_id = 0

    def execute_events(self) -> list:
        """
        Execute the events for this customer object and return the results in a list of the required format
        """

        for event in self.events:
            branch_id = event["branch"]

            if event["interface"] == "query":
                request = Request(
                    interface=Interface.Query,
                    id=self.id,
                    commit_id=self.commit_id
                )
            elif event["interface"] == "deposit":
                request = Request(
                    interface=Interface.Deposit,
                    id=self.id,
                    money=event["money"],
                    commit_id= self.commit_id
                )
            elif event["interface"] == "withdraw":
                request = Request(
                    interface=Interface.Withdraw,
                    id=self.id,
                    money=event["money"],
                    commit_id=self.commit_id
                )
            else:
                raise Exception("Invalid Event Type")
            response = self.stubs[branch_id].MsgDelivery(request)
            self.commit_id = response.commit_id
            self.recv_msg.append(response)

        return self.get_events_list()

    def get_events_list(self) -> list:
        """
        Returns the result of the events in the required format
        """

        event_list = []
        for msg in self.recv_msg:
            if msg.interface == Interface.Query:
                event_list.append({
                    "id": self.id,
                    "recv": [{
                        "interface": "query",
                        "branch": msg.id,
                        "balance": msg.money
                    }]
                })
            else:
                event_list.append({
                    "id": self.id,
                    "recv": [{
                        "interface": Interface.Name(msg.interface).lower(),
                        "branch": msg.id,
                        "result": ResponseStatus.Name(msg.status).lower()
                    }]
                })

        return event_list


def create_stub(branch_id: int) -> BranchStub:
    """
    Create a BranchStub used to communicate with the branch server for query, deposit, withdrawal
    """

    channel = grpc.insecure_channel(f'localhost:{start_port + branch_id}')
    return BranchStub(channel)
