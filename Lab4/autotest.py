import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')  # Выключаем визуальный режим
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://localhost:2443/login")

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

    username_field.send_keys("root")
    password_field.send_keys("0penBmc")
    password_field.send_keys(Keys.ENTER)

    old_url = driver.current_url
    assert wait.until(EC.url_changes(old_url))


def test_invalid_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://localhost:2443/login")

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

    username_field.send_keys("fvfsgrfgs")
    password_field.send_keys("0780jhjll")
    password_field.send_keys(Keys.ENTER)

    assert wait.until(EC.url_contains("next=/login"))


def test_login_block(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://localhost:2443/#/login")

    for _ in range(10):
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

        username_field.clear()
        password_field.clear()

        username_field.send_keys('operator')
        password_field.send_keys('wrongpassword')
        password_field.send_keys(Keys.ENTER)

        assert wait.until(EC.url_contains("next=/login"))

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))

    username_field.clear()
    password_field.clear()

    username_field.send_keys('operator')
    password_field.send_keys('password123')
    password_field.send_keys(Keys.ENTER)

    assert wait.until(EC.url_contains("next=/login"))
