# robotframework-libraryproxy

Simple library for calling robot framework keywords from Python. With the possibility that these call are also logged to the robot output.

Example Python library:

```python
from Browser import Browser
from robotlibraryproxy import library_proxy


class Dummy:
    def do_something_in_browser(self):
        with library_proxy(Browser) as browser:
            browser.new_browser(headless=False)
            browser.new_page("https://example.com")
            browser.click("text=More Information...")
```

Example Test case that uses this library:

```robotframework
*** Settings ***

Library    Dummy.py

# Library    Browser

*** Test Cases ***

a simple test
    Do Something In Browser

```

An excerpt from the Robot log:


![Example from robot log](doc/example_screenshot.png)

more comming soon...
