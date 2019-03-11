from typing import Any, Callable, IO, Iterator, Set, Tuple, Union

Obj = Any
Path = Tuple[Any, ...]
WalkType = Iterator[Tuple[Path, Obj]]
Cache = Set[int]
ObjI = Iterator[Tuple[Any, Any]]
ObjIFunc = Callable[[Obj], ObjI]
Stream = Union[str, IO[str]]
