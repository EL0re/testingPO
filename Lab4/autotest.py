import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException 
import time  


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--ignore-ssl-errors=yes')
    

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    driver.quit()


def test_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://127.0.0.1:2443/login")
    time.sleep(2)  

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    

    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    username_field.send_keys("root")
    password_field.send_keys("0penBmc")
    login_button.click()  

    wait.until(lambda driver: "/login" not in driver.current_url)
    assert "/login" not in driver.current_url


def test_invalid_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://127.0.0.1:2443/login")
    time.sleep(2) 

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  

    username_field.send_keys("fvfsgrfgs")
    password_field.send_keys("0780jhjll")
    login_button.click()


    time.sleep(3)
    assert "login" in driver.current_url


def test_login_block(driver):
    wait = WebDriverWait(driver, 10)
    
    for _ in range(10):
        driver.get("https://127.0.0.1:2443/#/login")
        time.sleep(2)  

        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  

        username_field.clear()
        password_field.clear()
        username_field.send_keys('operator')
        password_field.send_keys('wrongpassword')
        login_button.click() 
        
        time.sleep(2) 
        assert "login" in driver.current_url


    driver.get("https://127.0.0.1:2443/#/login")
    time.sleep(2)
    
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')  

    username_field.clear()
    password_field.clear()
    username_field.send_keys('operator')
    password_field.send_keys('password123')
    login_button.click()  
    
    time.sleep(3) 
    assert "login" in driver.current_url  