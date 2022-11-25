from __future__ import annotations

from types import TracebackType
from typing import Any, Dict, Generic, Optional, Protocol, Type, TypeVar, Union, cast, overload, runtime_checkable
from weakref import ref

from robot.libraries.BuiltIn import BuiltIn
from robot.running.context import EXECUTION_CONTEXTS
from robot.running.importer import Importer
from robot.running.model import Keyword

T = TypeVar("T")

_IMPORTER = Importer()


class _Proxy(Generic[T]):
    def __init__(self, name_or_type: Union[str, Type[T]], *args: str, **kwargs: str) -> None:
        self.__name_or_type = name_or_type
        self.__name = name_or_type if isinstance(name_or_type, str) else name_or_type.__name__
        self.__args = args
        self.__kwargs = kwargs
        self.__instance: Optional[ref[Any]] = None
        self.__real_instance: Optional[T] = None

    def __get_instance(self) -> T:
        if self.__instance is None or self.__instance() is None:
            if EXECUTION_CONTEXTS.current is None:
                self.__real_instance = _IMPORTER.import_library(
                    self.__name,
                    (
                        *self.__args,
                        *(f"{k}={str(v)}" for k, v in self.__kwargs.items()),
                    ),
                    None,
                    None,
                ).get_instance()

                self.__instance = ref(self.__real_instance)
            else:
                try:
                    self.__instance = ref(BuiltIn().get_library_instance(self.__name))
                except RuntimeError:

                    BuiltIn().import_library(
                        self.__name,
                        *(*self._Proxy__args, *(f"{k}={str(v)}" for k, v in self._Proxy__kwargs.items())),
                    )

                    self.__instance = ref(BuiltIn().get_library_instance(self.__name))

        return cast(T, self.__instance())

    def __getattr__(self, name: str) -> Any:
        if not name.startswith("_") and hasattr(self.__get_instance(), name):
            value = getattr(self.__get_instance(), name)

            if callable(value) and EXECUTION_CONTEXTS.current is not None:

                def call(*args: Any, **kwargs: Any) -> Any:
                    kw = Keyword(
                        f"{self.__name}.{name}",
                        args=(*args, *[f"{k}={str(v)}" for k, v in kwargs.items()]),
                    )

                    return kw.run(EXECUTION_CONTEXTS.current)

                return call

            return value

        raise AttributeError(name)


@runtime_checkable
class HasRobotLibraryProxy(Protocol):
    __robot_library_proxy: Optional[Dict[str, Any]]  # NOSONAR


class RobotLibraryProxy(Generic[T]):
    def __init__(self, name_or_type: Union[str, Type[T]], *args: str, **kwargs: str) -> None:
        self.__name_or_type = name_or_type
        self.__args = args
        self.__kwargs = kwargs
        self.robot_not_keyword = True
        self.__owner: Any = None
        self.__proxy: Optional[_Proxy[T]] = None

    def __set_name__(self, owner: Any, name: str) -> None:
        self.__owner = owner
        self.__owner_name = name

    @overload
    def __get__(self, obj: None, objtype: None) -> RobotLibraryProxy[T]:
        ...

    @overload
    def __get__(self, obj: object, objtype: type[object]) -> T:
        ...

    def __get__(self, obj: Any, objtype: Union[Type[Any], None]) -> Union[T, RobotLibraryProxy[T], None]:
        if obj is None:
            return self

        if not isinstance(obj, HasRobotLibraryProxy):
            cast(HasRobotLibraryProxy, obj).__robot_library_proxy = {}

        obj_with_proxy_data = cast(HasRobotLibraryProxy, obj)

        if self.__owner_name not in obj_with_proxy_data.__robot_library_proxy:
            obj_with_proxy_data.__robot_library_proxy[self.__owner_name] = cast(
                T, _Proxy(self.__name_or_type, *self.__args, **self.__kwargs)
            )

        return obj_with_proxy_data.__robot_library_proxy[self.__owner_name]

    def get_instance(self) -> T:
        if self.__proxy is None:
            self.__proxy = _Proxy(self.__name_or_type, *self.__args, **self.__kwargs)
        return cast(T, self.__proxy)

    def __enter__(self) -> T:
        return self.get_instance()

    @overload
    def __exit__(self, exc_type: None, exc_val: None, exc_tb: None) -> None:
        ...

    @overload
    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # do nothing
        pass


library_proxy = RobotLibraryProxy
