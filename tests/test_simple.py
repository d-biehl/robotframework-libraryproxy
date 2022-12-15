from pathlib import Path

from Browser import Browser
from Browser.utils.data_types import SupportedBrowsers
from robot.libraries.BuiltIn import BuiltIn
from robotlibraryproxy import RobotLibraryProxy, library_proxy

ROBOT_DATA_PATH = Path(Path(__file__).parent, "testdata", "robot")


def test_builtin() -> None:
    builtin = RobotLibraryProxy(BuiltIn).get_instance()  # type: ignore
    builtin.log("hello")
    print(builtin.ROBOT_LIBRARY_VERSION)


def test_builtin_with_named_parameter() -> None:
    builtin = RobotLibraryProxy(BuiltIn).get_instance()  # type: ignore
    builtin.log("hello", level="ERROR")


def test_something_in_browser() -> None:
    with library_proxy(Browser) as browser:  # type: ignore
        browser.new_page("https://example.com")
        browser.click("text=More Information...")


class TestClass:
    builtin: BuiltIn = library_proxy()
    browser: Browser = library_proxy(Browser)

    def log_something(self) -> None:
        self.builtin.log("done something")

    def do_something_in_browser(self) -> None:
        self.browser.new_browser(SupportedBrowsers.chromium, headless=True)
        self.browser.new_page("https://example.com")
        self.browser.click("text=More Information...")


def test_builtin_from_instance() -> None:
    instance = TestClass()
    instance.log_something()
    instance.builtin.log("hello from test")


def test_browser_from_instance() -> None:
    instance = TestClass()
    instance.do_something_in_browser()
    assert instance.browser.get_url() != "https://example.com"


def test_import_module() -> None:
    with library_proxy("testpackage") as mod:  # type: ignore
        mod.do_something_in_package()


def test_robot() -> None:
    from robot import run

    assert (
        run(
            str(ROBOT_DATA_PATH),
            outputdir=str(Path(ROBOT_DATA_PATH, "results")),
            # output=None,
            # log=None,
            # report=None,
            loglevel="TRACE:TRACE",
            console="quiet",
        )
        == 0
    )
