*** Settings ***
Library           ../lib/Dummy.py
Library           testpackage
# Library         Browser

*** Test Cases ***
first
    Do Something
    Log    1
    Log    2
    Log    2
    Log    2

second
    Do Something In Browser

third
    Do Something In Package
    BuiltIn.Evaluate    a
    testpackage.Do Something In Package
