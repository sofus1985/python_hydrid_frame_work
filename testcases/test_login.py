import pytest
from pages.LoginPage import LoginPage

@pytest.mark.usefixtures("setup")
class TestLogin:
    def test_login(self):
        login_page = LoginPage()
        login_page.enter_username("sdsr234@gmail.com")
        login_page.enter_password("NsN3RF@D4cU6J3")
        login_page.click_login()
        login_page.capture_screenshot("login_test")
        assert login_page.validation_url("https://tutorialsninja.com/demo/index.php?route=account/account")
