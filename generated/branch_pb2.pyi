from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Interface(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Query: _ClassVar[Interface]
    Withdraw: _ClassVar[Interface]
    Deposit: _ClassVar[Interface]
    Propagate_Withdraw: _ClassVar[Interface]
    Propagate_Deposit: _ClassVar[Interface]

class ResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Success: _ClassVar[ResponseStatus]
    Failure: _ClassVar[ResponseStatus]
Query: Interface
Withdraw: Interface
Deposit: Interface
Propagate_Withdraw: Interface
Propagate_Deposit: Interface
Success: ResponseStatus
Failure: ResponseStatus

class Request(_message.Message):
    __slots__ = ["interface", "id", "money"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    id: int
    money: int
    def __init__(self, interface: _Optional[_Union[Interface, str]] = ..., id: _Optional[int] = ..., money: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["interface", "id", "money", "status"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    id: int
    money: int
    status: ResponseStatus
    def __init__(self, interface: _Optional[_Union[Interface, str]] = ..., id: _Optional[int] = ..., money: _Optional[int] = ..., status: _Optional[_Union[ResponseStatus, str]] = ...) -> None: ...
