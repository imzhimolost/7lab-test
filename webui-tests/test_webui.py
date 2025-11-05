# webui-tests/test_webui.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Нет необходимости в SSL-опциях, так как используем HTTP
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_login_page_title(browser):
    browser.get("http://localhost:4430")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))
    assert "OpenBMC Mock WebUI" in browser.title

def test_successful_login(browser):
    browser.get("http://localhost:4430")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "username")))
    
    browser.find_element(By.ID, "username").send_keys("root")
    browser.find_element(By.ID, "password").send_keys("0penBmc")
    browser.find_element(By.ID, "login").click()
    
    # Ждём появления статуса успеха
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "status"))
    )
    assert "Успешный вход!" in browser.page_source