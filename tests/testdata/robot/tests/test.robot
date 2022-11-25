*** Settings ***
Library           ../lib/Dummy.py
Library           testpackage
# Library         Browser

*** Test Cases ***
first
    Do Something

second
    Do Something In Browser

third
    Do Something In Package
