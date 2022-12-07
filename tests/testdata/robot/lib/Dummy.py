from Browser import Browser
from Browser.utils.data_types import SupportedBrowsers
from robot.libraries.BuiltIn import BuiltIn
from robotlibraryproxy import library_proxy
from robot.api.deco import not_keyword


class Dummy:

    browser: Browser = library_proxy()

    def do_something(self) -> bool:
        print("do work")

        builtin: BuiltIn
        with library_proxy("BuiltIn") as builtin:
            builtin.log("hello")

        print("done")
        return True

    def do_something_in_browser(self) -> None:
        self.browser.new_browser(SupportedBrowsers.firefox, headless=False)
        self.browser.new_page("https://example.com")
        self.browser.click("text=More Information...")

    @not_keyword
    def not_a_keyword(self) -> None:
        print("not a keyword")
