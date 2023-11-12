import json

import grpc
from generated.branch_pb2_grpc import BranchStub
from generated.branch_pb2 import *
from utils import load_config_file

config = load_config_file()
start_port = config["start_port"]


class Customer:
    def __init__(self, id, customer_requests):
        # unique ID of the Customer
        self.id = id
        # customer requests from the input
        self.customer_requests = customer_requests
        # a list of received messages used for debugging purpose
        self.recv_msg: list[Response] = list()
        # pointer for the stub
        self.stub = self.create_stub()
        # counter for the logical clock
        self.logical_clock = 0
        # list of events on the branch along with clock values
        self.events: list[Event] = list()

    def create_stub(self) -> BranchStub:
        """
        Create a BranchStub used to communicate with the branch server for query, deposit, withdrawal
        """

        channel = grpc.insecure_channel(f'localhost:{start_port + self.id}')
        return BranchStub(channel)

    def execute_customer_requests(self):
        """
        Execute the customer requests for this customer object and print the results
        """

        for customer_request in self.customer_requests:
            interface: Interface
            # Increment clock for send event
            self.logical_clock += 1

            if customer_request["interface"] == "query":
                interface = Interface.Query
                request = Request(
                    interface=interface,
                    id=self.id,
                    customer_request_id=customer_request["customer-request-id"],
                    logical_clock=self.logical_clock
                )
            elif customer_request["interface"] == "deposit":
                interface = Interface.Deposit
                request = Request(
                    interface=interface,
                    id=self.id,
                    money=customer_request["money"],
                    customer_request_id=customer_request["customer-request-id"],
                    logical_clock=self.logical_clock
                )
            elif customer_request["interface"] == "withdraw":
                interface = Interface.Withdraw
                request = Request(
                    interface=interface,
                    id=self.id,
                    money=customer_request["money"],
                    customer_request_id=customer_request["customer-request-id"],
                    logical_clock=self.logical_clock
                )
            else:
                raise Exception("Invalid Request Type")

            self.recv_msg.append(self.stub.MsgDelivery(request))
            self.events.append(Event(
                customer_request_id=customer_request["customer-request-id"],
                logical_clock=self.logical_clock,
                interface=interface,
                comment=f"event_sent from customer {self.id}"
            ))

    def get_customer_events(self) -> EventList:
        """
        Get the customer events that incremented the logical clock
        """

        return EventList(id=self.id, type="customer", events=self.events)

    def get_branch_events(self) -> EventList:
        """
        Get all the branch events that incremented the logical clock in the branch associated with the customer
        """

        return self.stub.GetEvents(Empty())
