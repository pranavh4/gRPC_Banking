from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

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
    __slots__ = ["interface", "id", "money", "logical_clock", "customer_request_id"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_CLOCK_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    interface: Interface
    id: int
    money: int
    logical_clock: int
    customer_request_id: int
    def __init__(self, interface: _Optional[_Union[Interface, str]] = ..., id: _Optional[int] = ..., money: _Optional[int] = ..., logical_clock: _Optional[int] = ..., customer_request_id: _Optional[int] = ...) -> None: ...

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

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class EventList(_message.Message):
    __slots__ = ["id", "type", "events"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: str
    events: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(self, id: _Optional[int] = ..., type: _Optional[str] = ..., events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ["customer_request_id", "logical_clock", "interface", "comment"]
    CUSTOMER_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_CLOCK_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    customer_request_id: int
    logical_clock: int
    interface: Interface
    comment: str
    def __init__(self, customer_request_id: _Optional[int] = ..., logical_clock: _Optional[int] = ..., interface: _Optional[_Union[Interface, str]] = ..., comment: _Optional[str] = ...) -> None: ...
