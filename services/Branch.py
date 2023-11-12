from concurrent import futures

import grpc
from generated import branch_pb2, branch_pb2_grpc
from utils import load_config_file
from typing import Optional

config = load_config_file()
start_port = config["start_port"]


class Branch(branch_pb2_grpc.BranchServicer):

    def __init__(self, id: int, balance: int, branches: list):
        # unique ID of the Branch
        self.id: int = id
        # replica of the Branch's balance
        self.balance: int = balance
        # Dictionary of branches with their id as key
        self.branches: list = branches
        # the list of Branch stubs to communicate with the branches
        self.branch_stubs: list[branch_pb2_grpc.BranchStub] = self.create_branch_stubs()
        # a list of received messages used for debugging purpose
        self.recv_msg: list[branch_pb2.Response] = list()
        # counter for the logical clock
        self.logical_clock = 0
        # list of events on the branch along with clock values
        self.events: list[branch_pb2.Event] = list()

    def MsgDelivery(self, request: branch_pb2.Request, context) -> branch_pb2.Response:
        """
        Implement the various Branch to Branch and Branch to Customer Interfaces as listed below: \n
        - Branch.Query: Return the current balance
        - Branch.Withdraw: Withdraw some amount from the available balance and return status
        - Branch.Deposit: Deposit some amount and return the status
        - Branch.Propagate_Withdraw: Propagate the updated balance after withdrawal to all other branches
        - Branch.Propagate_Deposit: Propagate the updated balance after deposit to all other branches
        """

        # Increment logical clock for the reception event.
        # This can be receipt of request from a customer or another branch
        self.increment_clock(request)
        if request.interface in [branch_pb2.Interface.Propagate_Withdraw, branch_pb2.Interface.Propagate_Deposit]:
            request_sender = 'branch'
        else:
            request_sender = 'customer'

        self.events.append(branch_pb2.Event(
            customer_request_id=request.customer_request_id,
            logical_clock=self.logical_clock,
            interface=request.interface,
            comment=f"event_recv from {request_sender} {request.id}"
        ))

        # Implementation of Branch.Query interface
        if request.interface == branch_pb2.Interface.Query:
            return branch_pb2.Response(
                interface=request.interface,
                id=self.id,
                money=self.balance,
                status=branch_pb2.ResponseStatus.Success
            )

        # Implementation of Branch.Withdraw interface
        elif request.interface == branch_pb2.Interface.Withdraw:
            self.balance -= request.money

            # Broadcast the new balance to other branches
            if self.broadcast(branch_pb2.Interface.Propagate_Withdraw, request.customer_request_id):
                response_status = branch_pb2.ResponseStatus.Success
            else:
                response_status = branch_pb2.ResponseStatus.Failure

            return branch_pb2.Response(id=self.id, interface=request.interface, status=response_status)

        # Implementation of Branch.Deposit interface
        elif request.interface == branch_pb2.Interface.Deposit:
            self.balance += request.money

            # Broadcast the new balance to other branches
            if self.broadcast(branch_pb2.Interface.Propagate_Deposit, request.customer_request_id):
                response_status = branch_pb2.ResponseStatus.Success
            else:
                response_status = branch_pb2.ResponseStatus.Failure

            return branch_pb2.Response(id=self.id, interface=request.interface, status=response_status)

        # Implementation of Branch.Propagate_Withdraw interface
        elif request.interface == branch_pb2.Interface.Propagate_Withdraw:
            self.balance = request.money

            return branch_pb2.Response(
                id=self.id,
                interface=branch_pb2.Interface.Propagate_Withdraw,
                status=branch_pb2.ResponseStatus.Success
            )

        # Implementation of Branch.Propagate_Deposit interface
        elif request.interface == branch_pb2.Interface.Propagate_Deposit:
            self.balance = request.money

            return branch_pb2.Response(
                id=self.id,
                interface=branch_pb2.Interface.Propagate_Deposit,
                status=branch_pb2.ResponseStatus.Success
            )

        else:
            print(f"Received message with invalid interface: {request}")
            return branch_pb2.Response(status=branch_pb2.ResponseStatus.Failure)

    def GetEvents(self, request, context) -> branch_pb2.EventList:
        return branch_pb2.EventList(id=self.id, type="branch", events=self.events)

    def create_branch_stubs(self) -> list[branch_pb2_grpc.BranchStub]:
        """
        Create a list of branch stubs that can be used to propagate
        the updated balance to all branches after deposits/withdrawals
        """

        branch_stubs = []

        for branch in self.branches:
            # Skip creating stub for oneself
            if branch == start_port + self.id:
                continue

            channel = grpc.insecure_channel(f'localhost:{branch}')
            branch_stubs.append(branch_pb2_grpc.BranchStub(channel))

        return branch_stubs

    def broadcast(self, interface: branch_pb2.Interface, customer_request_id: int) -> bool:
        """
        Broadcast the balance to all the other branches
        :param interface: Propagate_Withdraw or Propagate_Deposit
        :param customer_request_id: ID of the customer that made the initial request
        """

        for branch_stub in self.branch_stubs:
            # Increment logical clock for send event
            self.increment_clock()
            # Instead of broadcasting the deposit/withdraw amount, we broadcast the new balance so that it is idempotent
            prop_request = branch_pb2.Request(
                interface=interface,
                id=self.id,
                money=self.balance,
                customer_request_id=customer_request_id,
                logical_clock=self.logical_clock
            )
            response: branch_pb2.Response = branch_stub.MsgDelivery(prop_request)
            self.recv_msg.append(response)
            self.events.append(branch_pb2.Event(
                customer_request_id=customer_request_id,
                logical_clock=self.logical_clock,
                interface=interface,
                comment=f"event_sent to branch {response.id}"
            ))

            if response.status == branch_pb2.ResponseStatus.Failure:
                print(f"Failure when {branch_pb2.Interface.Name(interface)} to other branches")
                return False

        return True

    def increment_clock(self, request: Optional[branch_pb2.Request] = None):
        if request:
            self.logical_clock = max(self.logical_clock, request.logical_clock) + 1
        else:
            self.logical_clock += 1

    def serve(self):
        """
        Create and return a grpc_server for this branch object
        """

        port = start_port + self.id
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        branch_pb2_grpc.add_BranchServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"BRANCH {self.id} started. Listening on port {port}")
        return server
