from concurrent import futures

import grpc
from generated import branch_pb2, branch_pb2_grpc
from utils import load_config_file

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

    def MsgDelivery(self, request: branch_pb2.Request, context):
        if request.interface == branch_pb2.Interface.Query:
            return branch_pb2.Response(
                interface=request.interface,
                id=self.id,
                money=self.balance,
                status=branch_pb2.ResponseStatus.Success
            )

        elif request.interface == branch_pb2.Interface.Withdraw:
            self.balance -= request.money

            # Broadcast the new balance to other branches
            if self.broadcast(branch_pb2.Interface.Propagate_Withdraw):
                response_status = branch_pb2.ResponseStatus.Success
            else:
                response_status = branch_pb2.ResponseStatus.Failure

            return branch_pb2.Response(interface=request.interface, status=response_status)

        elif request.interface == branch_pb2.Interface.Deposit:
            self.balance += request.money
            # Broadcast the new balance to other branches
            if self.broadcast(branch_pb2.Interface.Propagate_Deposit):
                response_status = branch_pb2.ResponseStatus.Success
            else:
                response_status = branch_pb2.ResponseStatus.Failure

            return branch_pb2.Response(interface=request.interface, status=response_status)

        elif request.interface == branch_pb2.Interface.Propagate_Withdraw:
            self.balance = request.money
            return branch_pb2.Response(
                interface=branch_pb2.Interface.Propagate_Withdraw,
                status=branch_pb2.ResponseStatus.Success
            )

        elif request.interface == branch_pb2.Interface.Propagate_Deposit:
            self.balance = request.money
            return branch_pb2.Response(
                interface=branch_pb2.Interface.Propagate_Deposit,
                status=branch_pb2.ResponseStatus.Success
            )

        else:
            print(f"Received message with invalid interface: {request}")
            return branch_pb2.Response(status=branch_pb2.ResponseStatus.Failure)

    def create_branch_stubs(self) -> list[branch_pb2_grpc.BranchStub]:
        branch_stubs = []

        for branch in self.branches:
            # Skip creating stub for oneself
            if branch == start_port + self.id:
                continue

            channel = grpc.insecure_channel(f'localhost:{branch}')
            branch_stubs.append(branch_pb2_grpc.BranchStub(channel))

        return branch_stubs

    def broadcast(self, interface: branch_pb2.Interface) -> bool:
        # Instead of broadcasting the deposit/withdraw amount, we broadcast the new balance so that it is idempotent
        prop_request = branch_pb2.Request(interface=interface, id=self.id, money=self.balance)

        for branch_stub in self.branch_stubs:
            response: branch_pb2.Response = branch_stub.MsgDelivery(prop_request)
            self.recv_msg.append(response)

            if response.status == branch_pb2.ResponseStatus.Failure:
                print(f"Failure when {branch_pb2.Interface.Name(interface)} to other branches")
                return False

        return True

    def serve(self):
        port = start_port + self.id
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        branch_pb2_grpc.add_BranchServicer_to_server(self, server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"BRANCH {self.id} started. Listening on port {port}")
        return server
