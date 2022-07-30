from datetime import datetime
from enum import Enum
from typing import Any, List, Dict, Callable, Type, cast, Optional, TypeVar

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any = None) -> Optional[int]:
    return x


def from_timestamp(x: Any = None) -> Optional[datetime]:
    return datetime.fromtimestamp(x)


def date_to_timestamp(x: datetime = None) -> Optional[int]:
    return round(x.timestamp())


def from_str(x: Any = None) -> Optional[str]:
    return x


def from_bool(x: Any = None) -> Optional[bool]:
    if not x:
        return False
    return x


def from_none(x: Any = None) -> Any:
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any = None) -> Optional[List[T]]:
    if not x:
        return None
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_list_error(f: Callable[[Any], T], x: Any = None) -> Optional[List[T]]:
    if not x:
        return None

    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any = None) -> Any:
    if not x:
        return None
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any = None) -> Any:
    if not x:
        return None
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any = None) -> Dict[str, T]:
    assert isinstance(x, dict)
    return {k: f(v) for (k, v) in x.items()}
