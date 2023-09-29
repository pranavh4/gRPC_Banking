from concurrent import futures

import grpc
from generated import *


class Branch(branch_pb2_grpc.BranchServicer):

    def __init__(self, id: int, balance: int, branches: dict):
        # unique ID of the Branch
        self.id: int = id
        # replica of the Branch's balance
        self.balance: int = balance
        # Dictionary of branches with their id as key
        self.branches: dict = branches
        # the dictionary of Branch stubs to communicate with the branches
        self.stub_dict: dict = {}
        for branch in branches.values():
            channel = grpc.insecure_channel(f'localhost:{branch["port"]}')
            self.stub_dict[branch["id"]] = branch_pb2_grpc.BranchStub(channel)

        # a list of received messages used for debugging purpose
        self.recvMsg: list = list()

    def Deposit(self, request, context):
        self.balance += request.amount

        for branch_id in self.branches.keys():
            if branch_id == self.id:
                continue

            prop_balance = branch_pb2.Balance(customer_id=request.customer_id, money=self.balance)
            response: branch_pb2.PropagateResponse = self.stub_dict[branch_id].Propagate_Deposit(prop_balance)

            if response.message != "Success":
                raise Exception(f"Failure when propagating deposit to branch {branch_id}")

        return branch_pb2.TransactionResponse(interface="deposit", result="Success")

    def Withdraw(self, request, context):
        self.balance -= request.amount

        for branch_id in self.branches.keys():
            if branch_id == self.id:
                continue

            prop_balance = branch_pb2.Balance(customer_id=request.customer_id, money=self.balance)
            response: branch_pb2.PropagateResponse = self.stub_dict[branch_id].Propagate_Withdraw(prop_balance)

            if response.message != "Success":
                raise Exception(f"Failure when propagating withdraw to branch {branch_id}")

        return branch_pb2.TransactionResponse(interface="withdraw", result="Success")
        return branch_pb2.TransactionResponse(interface="withdraw", result="Success")

    def Query(self, request, context):
        return branch_pb2.Balance(customer_id=request.customer_id, money=self.balance)

    def Propagate_Deposit(self, request, context):
        branch_id = request.customer_id
        self.branches[branch_id]["balance"] = request.money
        return branch_pb2.PropagateResponse(message="Success")

    def Propagate_Withdraw(self, request, context):
        branch_id = request.customer_id
        self.branches[branch_id]["balance"] = request.money
        return branch_pb2.PropagateResponse(message="Success")

    @staticmethod
    def serve(id, balance: int, branches: dict, port: int):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        branch_pb2_grpc.add_BranchServicer_to_server(Branch(id, balance, branches), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"BRANCH {id} started. Listening on port {port}")
        return server
