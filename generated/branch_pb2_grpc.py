# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import branch_pb2 as branch__pb2


class BranchStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MsgDelivery = channel.unary_unary(
                '/Branch/MsgDelivery',
                request_serializer=branch__pb2.Request.SerializeToString,
                response_deserializer=branch__pb2.Response.FromString,
                )
        self.GetEvents = channel.unary_unary(
                '/Branch/GetEvents',
                request_serializer=branch__pb2.Empty.SerializeToString,
                response_deserializer=branch__pb2.EventList.FromString,
                )


class BranchServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MsgDelivery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEvents(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BranchServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MsgDelivery': grpc.unary_unary_rpc_method_handler(
                    servicer.MsgDelivery,
                    request_deserializer=branch__pb2.Request.FromString,
                    response_serializer=branch__pb2.Response.SerializeToString,
            ),
            'GetEvents': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEvents,
                    request_deserializer=branch__pb2.Empty.FromString,
                    response_serializer=branch__pb2.EventList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Branch', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Branch(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MsgDelivery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Branch/MsgDelivery',
            branch__pb2.Request.SerializeToString,
            branch__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEvents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Branch/GetEvents',
            branch__pb2.Empty.SerializeToString,
            branch__pb2.EventList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
