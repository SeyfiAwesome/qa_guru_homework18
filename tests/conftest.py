import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import attach
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        default="false",
        choices=("true", "false"),
        help="Run browser in headless mode"
    )
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to use for testing"
    )
    parser.addoption(
        "--browser_version",
        default="128.0",
        help="Version of the test browser"
    )
    parser.addoption(
        "--base-url",
        default="https://demoqa.com",
        help="Base application URL"
    )
    parser.addoption(
        "--selenoid-url",
        default="selenoid.autotests.cloud/wd/hub",
        help="Selenoid hub URL"
    )
    parser.addoption(
        "--window-size",
        default="1920,1080",
        choices=(
            "1920,1080",
            "1280,720",
            "768,1024",
        ),
        help="Browser window dimensions"
    )


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    hub_login = os.getenv("SELENOID_LOGIN")
    hub_password = os.getenv("SELENOID_PASSWORD")

    headless_flag = request.config.getoption("--headless") == "true"
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")
    base_url = request.config.getoption("--base-url")
    selenoid_url = request.config.getoption("--selenoid-url")
    window_size = request.config.getoption("--window-size")

    if not hub_login or not hub_password:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()

        if headless_flag:
            options.add_argument("--headless")

        options.add_argument(f"--window-size={window_size}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        browser.config.driver = driver
        browser.config.base_url = base_url

        yield browser

        attach.take_screenshot(driver)
        attach.save_page_html(driver)
        attach.save_browser_logs(driver)
        attach.add_test_video(driver)

        driver.quit()
    else:
        options = Options()

        if headless_flag:
            options.add_argument("--headless")

        options.add_argument(f"--window-size={window_size}")

        selenoid_capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }
        options.capabilities.update(selenoid_capabilities)

        driver = webdriver.Remote(
            command_executor=f"https://{hub_login}:{hub_password}@{selenoid_url}",
            options=options
        )

        browser.config.driver = driver
        browser.config.base_url = base_url

        yield browser

        attach.take_screenshot(driver)
        attach.save_page_html(driver)
        attach.save_browser_logs(driver)
        attach.add_test_video(driver)

        driver.quit()


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()