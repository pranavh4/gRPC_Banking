# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: branch.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62ranch.proto\"#\n\x0cQueryRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\"9\n\x12TransactionRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x05\"8\n\x13TransactionResponse\x12\x11\n\tinterface\x18\x01 \x01(\t\x12\x0e\n\x06result\x18\x02 \x01(\t\"$\n\x11PropagateResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"-\n\x07\x42\x61lance\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\r\n\x05money\x18\x02 \x01(\x05\x32\x88\x02\n\x06\x42ranch\x12\"\n\x05Query\x12\r.QueryRequest\x1a\x08.Balance\"\x00\x12\x36\n\x07\x44\x65posit\x12\x13.TransactionRequest\x1a\x14.TransactionResponse\"\x00\x12\x37\n\x08Withdraw\x12\x13.TransactionRequest\x1a\x14.TransactionResponse\"\x00\x12\x34\n\x12Propagate_Withdraw\x12\x08.Balance\x1a\x12.PropagateResponse\"\x00\x12\x33\n\x11Propagate_Deposit\x12\x08.Balance\x1a\x12.PropagateResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'branch_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_QUERYREQUEST']._serialized_start=16
  _globals['_QUERYREQUEST']._serialized_end=51
  _globals['_TRANSACTIONREQUEST']._serialized_start=53
  _globals['_TRANSACTIONREQUEST']._serialized_end=110
  _globals['_TRANSACTIONRESPONSE']._serialized_start=112
  _globals['_TRANSACTIONRESPONSE']._serialized_end=168
  _globals['_PROPAGATERESPONSE']._serialized_start=170
  _globals['_PROPAGATERESPONSE']._serialized_end=206
  _globals['_BALANCE']._serialized_start=208
  _globals['_BALANCE']._serialized_end=253
  _globals['_BRANCH']._serialized_start=256
  _globals['_BRANCH']._serialized_end=520
# @@protoc_insertion_point(module_scope)
