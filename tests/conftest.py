import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import attach


def pytest_addoption(parser):
    parser.addoption(
        '--browser_mode',
        default='normal',
        choices=('normal', 'invisible'),
        help="Run browser in normal or headless mode"
    )
    parser.addoption(
        "--test_browser",
        default='chrome',
        help="Browser to use for testing"
    )
    parser.addoption(
        "--browser_ver",
        default="128.0",
        help="Version of the test browser"
    )
    parser.addoption(
        "--app_url",
        default='https://demoqa.com',
        help='Base application URL'
    )
    parser.addoption(
        '--remote_hub',
        default='selenoid.autotests.cloud/wd/hub',
        help="Selenoid hub URL"
    )
    parser.addoption(
        '--screen_resolution',
        default='1920,1080',
        choices=(
            "1920,1080",
            "1280,720",
            "768,1024",
        ),
        help='Browser window dimensions'
    )


@pytest.fixture(scope='function', autouse=True)
def manage_browser(request):
    hub_login = os.getenv("SELENOID_LOGIN")
    hub_password = os.getenv("SELENOID_PASSWORD")

    target_browser = request.config.getoption('--test_browser')
    target_version = request.config.getoption("--browser_ver")
    invisible_mode = request.config.getoption("--browser_mode") == "invisible"
    site_base = request.config.getoption("--app_url")
    selenoid_endpoint = request.config.getoption("--remote_hub")
    viewport = request.config.getoption("--screen_resolution")

    browser_prefs = Options()

    if invisible_mode:
        browser_prefs.add_argument("--headless")

    browser_prefs.add_argument(f"--window-size={viewport}")

    remote_capabilities = {
        "browserName": target_browser,
        "browserVersion": target_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    browser_prefs.capabilities.update(remote_capabilities)

    web_driver = webdriver.Remote(
        command_executor=f"https://{hub_login}:{hub_password}@{selenoid_endpoint}",
        options=browser_prefs
    )

    browser.config.driver = web_driver
    browser.config.base_url = site_base

    yield browser

    attach.take_screenshot(web_driver)
    attach.save_page_html(web_driver)
    attach.save_browser_logs(web_driver)
    attach.add_test_video(web_driver)

    web_driver.quit()


@pytest.fixture(scope="session", autouse=True)
def load_environment():
    load_dotenv()
