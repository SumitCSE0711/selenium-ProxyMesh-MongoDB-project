import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pymongo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_scraper"]
collection = db["tweets"]

logging.basicConfig(level=logging.INFO)

twitter_username = "your_username"  # pls provide your twitter username
twitter_password = "your_password"  # pls provide your twitter password

def create_driver():
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def login_to_twitter(driver):
    driver.get("https://twitter.com/login")
    time.sleep(3)  

    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(twitter_username)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    time.sleep(2)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(twitter_password)
    driver.find_element(By.XPATH, "//span[text()='Log in']").click()

    time.sleep(3)  
    logging.info("Login successful!")

def scrape_twitter_data():
    driver = create_driver()
    
    try:
        login_to_twitter(driver)  
        
        driver.get("https://twitter.com/explore/tabs/trending") 
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='trend']")))

        time.sleep(5)  

        trends = []
        trend_elements = driver.find_elements(By.XPATH, "//div[@data-testid='trend']//span[contains(@class, 'r-poiln3')]")
        
        for trend in trend_elements[:25]:
            trend_text = trend.text.strip()
            if trend_text and trend_text != '':
                trends.append(trend_text)

        logging.info(f"Trends found: {trends}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "timestamp": timestamp,
            "trends": trends
        }
        collection.insert_one(data)  

        driver.quit() 
        return trends, timestamp

    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        driver.quit()  
        return [], None
