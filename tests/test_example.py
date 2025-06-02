import pytest
from playwright.sync_api import Page


def test_example(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/")
    assert page.title() == "OrangeHRM"
