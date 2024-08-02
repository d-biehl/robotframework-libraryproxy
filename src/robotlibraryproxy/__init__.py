from __future__ import annotations

from types import TracebackType
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Optional,
    Protocol,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_type_hints,
    overload,
    runtime_checkable,
)
from weakref import ref

from robot.version import get_version
from robot.libraries.BuiltIn import BuiltIn
from robot.running.context import EXECUTION_CONTEXTS
from robot.running.importer import Importer
from robot.running.librarykeywordrunner import LibraryKeywordRunner
from robot.running.model import Keyword
from robot.running.statusreporter import StatusReporter

T = TypeVar("T")

_IMPORTER = Importer()


def get_robot_version() -> Tuple[int, ...]:
    return tuple(int(i) for i in get_version(naked=True).split("."))


if get_robot_version() >= (7, 0):
    from robot.result import Keyword as KeywordResult
    from robot.running.model import Keyword as KeywordData
    from robot.variables import VariableAssignment

    class LibraryKeywordRunnerWrapper(LibraryKeywordRunner):
        def __init__(self, runner: LibraryKeywordRunner, callable: Callable[..., Any], *args: Any, **kwargs: Any):
            self._runner = runner
            self.name = runner.name
            self.keyword = runner.keyword
            self.languages = runner.languages
            self.pre_run_messages = runner.pre_run_messages
            self._callable = callable
            self._args = args
            self._kwargs = kwargs

        def run(self, data: KeywordData, result: KeywordResult, context, run=True):  # type: ignore
            kw = self.keyword.bind(data)
            assignment = VariableAssignment(data.assign)
            self._config_result(result, data, kw, assignment)

            with StatusReporter(data, result, context, run, implementation=kw):
                if run:
                    return self._callable(*self._args, **self._kwargs)

    class KeywordWrapper(Keyword):
        def __init__(
            self,
            name: str,
            callable: Callable[..., Any],
            *args: Any,
            **kwargs: Any,
        ):
            self._callable = callable
            self._args = args
            self._kwargs = kwargs

            super().__init__(name, args=(*args, *[f"{k}={str(v)}" for k, v in kwargs.items()]))

        def run(self, result, context, run=True, templated=None):  # type: ignore
            runner = context.get_runner(self.name)
            if context.dry_run:
                return None
            if isinstance(runner, LibraryKeywordRunner):
                runner = LibraryKeywordRunnerWrapper(runner, self._callable, *self._args, **self._kwargs)
            return runner.run(self, result.body.create_keyword(), context)

else:

    class LibraryKeywordRunnerWrapper(LibraryKeywordRunner):  # type: ignore
        def __init__(self, runner: LibraryKeywordRunner, callable: Callable[..., Any], *args: Any, **kwargs: Any):
            self._runner = runner
            self._handler = runner._handler
            self.name = runner.name
            self.pre_run_messages = runner.pre_run_messages
            self._callable = callable
            self._args = args
            self._kwargs = kwargs

        def run(self, kw: Any, context: Any, run: bool = True) -> Any:

            result = self._runner._get_result(kw, ())

            with StatusReporter(kw, result, context, run):
                if run:
                    return self._callable(*self._args, **self._kwargs)

    class KeywordWrapper(Keyword):  # type: ignore
        def __init__(
            self,
            name: str,
            callable: Callable[..., Any],
            *args: Any,
            **kwargs: Any,
        ):
            self._callable = callable
            self._args = args
            self._kwargs = kwargs

            super().__init__(name, args=(*args, *[f"{k}={str(v)}" for k, v in kwargs.items()]))

        def run(self, context: Any, run: bool = True, templated: Any = None) -> Any:
            runner = context.get_runner(self.name)
            if isinstance(runner, LibraryKeywordRunner):
                runner = LibraryKeywordRunnerWrapper(runner, self._callable, *self._args, **self._kwargs)
            return runner.run(self, context)


class _Proxy(Generic[T]):
    def __init__(self, name_or_type: Union[str, Type[T]], *args: str, **kwargs: str) -> None:
        self.__name_or_type = name_or_type
        self.__name = name_or_type if isinstance(name_or_type, str) else name_or_type.__name__
        self.__args = args
        self.__kwargs = kwargs
        self.__instance: Optional[ref[Any]] = None
        self.__real_instance: Optional[T] = None

    if get_robot_version() >= (7, 0):

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
                    ).instance

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
                        result = EXECUTION_CONTEXTS.current.steps[-1][1] if EXECUTION_CONTEXTS.current.steps else None

                        if result is None:
                            result = EXECUTION_CONTEXTS.current.test or EXECUTION_CONTEXTS.current.suite

                        return KeywordWrapper(f"{self.__name}.{name}", value, *args, **kwargs).run(
                            result, EXECUTION_CONTEXTS.current
                        )  # type: ignore

                    return call

                return value

            raise AttributeError(name)

    else:

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
                        return KeywordWrapper(f"{self.__name}.{name}", value, *args, **kwargs).run(
                            EXECUTION_CONTEXTS.current
                        )  # type: ignore

                    return call

                return value

            raise AttributeError(name)


@runtime_checkable
class HasRobotLibraryProxy(Protocol):
    __robot_library_proxy: Dict[str, Any]  # NOSONAR


class RobotLibraryProxy(Generic[T]):
    def __init__(self, name_or_type: Union[str, Type[T], None] = None, *args: str, **kwargs: str) -> None:
        self.__name_or_type = name_or_type
        self.__args = args
        self.__kwargs = kwargs
        self.robot_not_keyword = True
        self.__owner: Any = None
        self.__proxy: Optional[_Proxy[T]] = None

    def __set_name__(self, owner: Any, name: str) -> None:
        self.__owner = owner
        self.__owner_name = name
        if self.__name_or_type is None:
            hints = get_type_hints(owner)
            hint = hints.get(name, None)
            self.__name_or_type = hint

    @overload
    def __get__(self, obj: None, objtype: None) -> RobotLibraryProxy[T]:
        ...

    @overload
    def __get__(self, obj: object, objtype: type[object]) -> T: ...

    def __get__(self, obj: Any, objtype: Union[Type[Any], None]) -> Union[T, RobotLibraryProxy[T], None]:
        if obj is None:
            return self

        if not isinstance(obj, HasRobotLibraryProxy) or obj.__robot_library_proxy is None:
            obj.__robot_library_proxy = {}

        obj_with_proxy_data = cast(HasRobotLibraryProxy, obj)

        if self.__owner_name not in obj_with_proxy_data.__robot_library_proxy:
            obj_with_proxy_data.__robot_library_proxy[self.__owner_name] = cast(
                T, _Proxy(self.__name_or_type, *self.__args, **self.__kwargs)  # type: ignore
            )

        return cast(T, obj_with_proxy_data.__robot_library_proxy[self.__owner_name])

    def get_instance(self) -> T:
        if self.__proxy is None:
            self.__proxy = _Proxy(self.__name_or_type, *self.__args, **self.__kwargs)  # type: ignore
        return cast(T, self.__proxy)

    def __enter__(self) -> T:
        return self.get_instance()

    @overload
    def __exit__(self, exc_type: None, exc_val: None, exc_tb: None) -> None: ...

    @overload
    def __exit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        # do nothing
        pass


library_proxy = RobotLibraryProxy
