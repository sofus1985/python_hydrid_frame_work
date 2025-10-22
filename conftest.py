import pytest
import pytest_html
from base.Base import Base
from utilities.ReadConfig import ReadConfig
from utilities.Logger import Logger

logger = Logger.get_logger()

# ------------------------------
# Fixture: Setup browser once per test class
# ------------------------------
@pytest.fixture(scope="class")
def setup(request):
    # Initialize the driver only once per test class
    base = Base(browser=ReadConfig.getBrowser(), url=ReadConfig.getApplicationURL())
    request.cls.driver = base.driver
    request.cls.base = base
    yield
    base.quit()
    logger.info("Browser closed")

# ------------------------------
# Hook: Capture screenshot on failure
# ------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if hasattr(item.cls, "base"):
            screenshot = item.cls.base.capture_screenshot(item.name)
            if screenshot:
                report.extra = getattr(report, "extra", [])
                report.extra.append(pytest_html.extras.image(screenshot))


