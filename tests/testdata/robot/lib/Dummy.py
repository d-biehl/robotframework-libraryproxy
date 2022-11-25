from Browser import Browser
from robot.libraries.BuiltIn import BuiltIn
from robotlibraryproxy import library_proxy


class Dummy:

    browser: Browser = library_proxy(Browser)

    def do_something(self) -> bool:
        print("do work")

        builtin: BuiltIn
        with library_proxy("BuiltIn") as builtin:
            builtin.log("hello")

        print("done")
        return True

    def do_something_in_browser(self) -> None:
        self.browser.new_page("https://example.com")
        self.browser.click("text=More Information...")
