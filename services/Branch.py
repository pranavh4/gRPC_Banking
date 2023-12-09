import threading
import time
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
        # the current commit id, indicating how caught up the branch is
        self.commit_id: int = 0
        # Callback to handle async result of propagate events
        self.propagate_callback = PropagateCallback(self)
        # lock to be acquired for critical sections
        self.lock: threading.Lock = threading.Lock()
        # List storing the outstanding updates
        self.outstanding_updates: list[branch_pb2.Request] = list()
        # Run thread in background that periodically applies any outstanding updates
        threading.Thread(daemon=True, target=self.apply_outstanding_updates).start()

    def MsgDelivery(self, request: branch_pb2.Request, context):
        """
        Implement the various Branch to Branch and Branch to Customer Interfaces as listed below: \n
        - Branch.Query: Return the current balance
        - Branch.Withdraw: Withdraw some amount from the available balance and return status
        - Branch.Deposit: Deposit some amount and return the status
        - Branch.Propagate_Withdraw: Propagate the updated balance after withdrawal to all other branches
        - Branch.Propagate_Deposit: Propagate the updated balance after deposit to all other branches
        """

        # Implementation of Branch.Query interface
        if request.interface == branch_pb2.Interface.Query:
            # Wait till branch has received all updates till commit_id
            self.await_update(request.commit_id)

            return branch_pb2.Response(
                interface=request.interface,
                id=self.id,
                money=self.balance,
                commit_id=self.commit_id,
                status=branch_pb2.ResponseStatus.Success
            )

        # Implementation of Branch.Withdraw interface
        elif request.interface == branch_pb2.Interface.Withdraw:
            # Wait till branch has received all updates till commit_id
            self.await_update(request.commit_id)

            self.lock.acquire(blocking=True)
            self.balance -= request.money
            self.commit_id += 1
            self.lock.release()

            # Broadcast the new balance to other branches
            self.broadcast(branch_pb2.Interface.Propagate_Withdraw)
            response_status = branch_pb2.ResponseStatus.Success

            return branch_pb2.Response(
                id=self.id,
                interface=request.interface,
                commit_id=self.commit_id,
                status=response_status
            )

        # Implementation of Branch.Deposit interface
        elif request.interface == branch_pb2.Interface.Deposit:
            # Wait till branch has received all updates till commit_id
            self.await_update(request.commit_id)

            self.lock.acquire(blocking=True)
            self.balance += request.money
            self.commit_id += 1
            self.lock.release()

            # Broadcast the new balance to other branches
            self.broadcast(branch_pb2.Interface.Propagate_Deposit)
            response_status = branch_pb2.ResponseStatus.Success

            return branch_pb2.Response(
                id=self.id,
                interface=request.interface,
                commit_id=self.commit_id,
                status=response_status
            )

        # Implementation of Branch.Propagate_Withdraw and Branch.Propagate_Deposit interface
        elif (request.interface == branch_pb2.Interface.Propagate_Withdraw or
              request.interface == branch_pb2.Interface.Propagate_Deposit):
            insert_idx = 0
            for i, update in enumerate(self.outstanding_updates):
                if update.commit_id > request.commit_id:
                    break
                insert_idx += 1

            self.outstanding_updates.insert(insert_idx, request)

            return branch_pb2.Response(
                id=self.id,
                interface=branch_pb2.Interface.Propagate_Withdraw,
                status=branch_pb2.ResponseStatus.Success
            )

        else:
            print(f"Received message with invalid interface: {request}")
            return branch_pb2.Response(id=self.id, status=branch_pb2.ResponseStatus.Failure)

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

    def broadcast(self, interface: branch_pb2.Interface):
        """
        Broadcast the balance to all the other branches
        :param interface: Propagate_Withdraw or Propagate_Deposit
        """

        # Instead of broadcasting the deposit/withdraw amount, we broadcast the new balance so that it is idempotent
        prop_request = branch_pb2.Request(
            interface=interface,
            id=self.id,
            money=self.balance,
            commit_id=self.commit_id
        )

        for branch_stub in self.branch_stubs:
            future: grpc.Future = branch_stub.MsgDelivery.future(prop_request)
            future.add_done_callback(self.propagate_callback)

    def await_update(self, commit_id: int):
        """
        Block till the branch has caught up till commit_id
        """

        if self.commit_id >= commit_id:
            return

        print(f"Branch {self.id} waiting to get all updates upto commit id: {commit_id}")

        while self.commit_id < commit_id:
            time.sleep(0.5)

        print(f"Branch {self.id} got all updates upto commit id: {commit_id}")

    #
    def apply_outstanding_updates(self):
        """
        Check if any outstanding updates are present and apply them to this branch
        """

        while True:
            time.sleep(0.1)
            self.lock.acquire(blocking=True)
            idx = 0

            for update in self.outstanding_updates:
                if update.commit_id != self.commit_id + 1:
                    break

                self.balance = update.money
                self.commit_id = update.commit_id
                idx += 1

            self.outstanding_updates = self.outstanding_updates[idx:]
            self.lock.release()

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


class PropagateCallback:
    def __init__(self, branch: Branch):
        self.branch = branch
        # To prevent multiple callbacks from updating recv_msg concurrently
        self.lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        future: grpc.Future = args[0]
        result = future.result()

        if result.status == branch_pb2.ResponseStatus.Failure:
            print(f"Failure when propagating to other branches")

        self.lock.acquire(blocking=True)
        self.branch.recv_msg.append(result)
        self.lock.release()
