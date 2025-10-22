import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException
)
from utilities.ReadConfig import ReadConfig
from utilities.Logger import Logger

logger = Logger.get_logger()

class Base:
    driver = None
    web_driver_wait = None
    fluent_wait = None

    def __init__(self, browser: str = None, url: str = None):
        self.browser = browser.lower() if browser else ReadConfig.getBrowser().lower()
        self.base_url = url if url else ReadConfig.getApplicationURL()
        self.driver = self._init_driver()
        self.driver.delete_all_cookies()
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(ReadConfig.getImplicitWait())

        # Fluent wait
        self.fluent_wait = WebDriverWait(
            self.driver,
            ReadConfig.getFluentTimeout(),
            ReadConfig.getFluentPoll(),
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotInteractableException,
                ElementClickInterceptedException
            ]
        )

        self.js_driver = self.driver
        self.actions = ActionChains(self.driver)

    # ------------------------------
    # Driver Initialization
    # ------------------------------
    def _init_driver(self):
        driver = None
        if self.browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--incognito")
            options.page_load_strategy = "normal"
            options.add_experimental_option("excludeSwitches", ["enable-automation", "disable-infoBars"])
            driver = webdriver.Chrome(service=ChromeService(), options=options)

        elif self.browser == "firefox":
            options = FirefoxOptions()
            options.page_load_strategy = "eager"
            driver = webdriver.Firefox(service=FirefoxService(), options=options)

        elif self.browser == "edge":
            options = EdgeOptions()
            options.page_load_strategy = "eager"
            options.add_experimental_option("excludeSwitches", ["enable-automation", "disable-infoBars"])
            driver = webdriver.Edge(service=EdgeService(), options=options)

        else:
            raise ValueError(f"Unsupported browser: {self.browser}")

        self.web_driver_wait = WebDriverWait(driver, 10)
        return driver

    # ------------------------------
    # Selenium Actions
    # ------------------------------
    def click(self, locator):
        element = self.fluent_wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text: str):
        element = self.fluent_wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        element = self.fluent_wait.until(EC.visibility_of_element_located(locator))
        return element.text.strip()

    def is_visible(self, locator) -> bool:
        try:
            return self.fluent_wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except TimeoutException:
            return False

    def hover_over_element(self, locator):
        element = self.fluent_wait.until(EC.visibility_of_element_located(locator))
        self.actions.move_to_element(element).perform()

    def safe_click(self, locator):
        try:
            self.click(locator)
        except (ElementClickInterceptedException, StaleElementReferenceException, TimeoutException):
            logger.info("Retrying click with JavaScript executor")
            self.js_click(locator)

    # ------------------------------
    # Dropdowns
    # ------------------------------
    def select_by_visible_text(self, locator, text: str):
        element = self.fluent_wait.until(EC.visibility_of_element_located(locator))
        Select(element).select_by_visible_text(text)

    def select_by_index(self, locator, index: int):
        element = self.fluent_wait.until(EC.visibility_of_element_located(locator))
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value: str):
        element = self.fluent_wait.until(EC.visibility_of_element_located(locator))
        Select(element).select_by_value(value)

    # ------------------------------
    # Frames & Tabs
    # ------------------------------
    def switch_to_frame(self, locator):
        frame = self.fluent_wait.until(EC.visibility_of_element_located(locator))
        self.driver.switch_to.frame(frame)

    def switch_to_parent_frame(self):
        self.driver.switch_to.default_content()

    def switch_to_new_tab(self):
        parent_handle = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if handle != parent_handle:
                self.driver.switch_to.window(handle)

    # ------------------------------
    # JavaScript Executor
    # ------------------------------
    def js_click(self, locator):
        element = self.driver.find_element(*locator)
        self.js_driver.execute_script("arguments[0].click();", element)

    def js_set_attribute(self, locator, attribute: str, value: str):
        element = self.driver.find_element(*locator)
        self.js_driver.execute_script(
            "arguments[0].setAttribute(arguments[1], arguments[2]);", element, attribute, value
        )

    def js_get_inner_text(self, locator) -> str:
        element = self.driver.find_element(*locator)
        return self.js_driver.execute_script("return arguments[0].innerText;", element).strip()

    # ------------------------------
    # Screenshots
    # ------------------------------
    def capture_screenshot(self, test_name: str):
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        file_path = os.path.join(screenshots_dir, f"{test_name}.png")
        self.driver.save_screenshot(file_path)
        logger.info(f"Screenshot saved: {file_path}")
        return file_path

    # ------------------------------
    # URL Validation
    # ------------------------------
    def validation_url(self, expected_url: str) -> bool:
        return self.driver.current_url.lower() == expected_url.lower()

    # ------------------------------
    # Quit Browser
    # ------------------------------
    def quit(self):
        if self.driver:
            self.driver.quit()
            self.driver = None



