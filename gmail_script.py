import time
import random
import csv
import os
import logging
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from faker import Faker

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Initialize Faker for random names
fake = Faker()

# CSV File for storing created accounts
ACCOUNTS_FILE = "created_accounts.csv"

# Load proxies dynamically from a file
def load_proxies():
    try:
        with open("proxies.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error("Proxies file not found!")
        return []

PROXY_LIST = load_proxies()

# Get a random proxy from the list
def get_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

# Save created Gmail accounts to CSV
def save_account(email, proxy):
    file_exists = os.path.exists(ACCOUNTS_FILE)

    with open(ACCOUNTS_FILE, "a", newline="") as csvfile:
        fieldnames = ["Email", "Proxy", "Time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({"Email": email, "Proxy": proxy, "Time": time.strftime("%Y-%m-%d %H:%M:%S")})

# Function to create a Gmail account
def create_gmail_account(password):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f"{first_name.lower()}{last_name.lower()}{random.randint(1000,9999)}"
    email = f"{username}@gmail.com"

    proxy = get_proxy()
    logging.info(f"Creating account: {email} using proxy: {proxy if proxy else 'No Proxy'}")

    driver = None  # Initialize driver variable

    try:
        options = webdriver.ChromeOptions()
        options.binary_location = "/data/data/com.termux/files/usr/bin/chromium"  # Set Chromium binary location

        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = uc.Chrome(options=options)  # Initialize driver
        wait = WebDriverWait(driver, 15)

        # Open Gmail Signup Page
        driver.get("https://accounts.google.com/signup")

        # Fill out the form
        wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(first_name)
        wait.until(EC.presence_of_element_located((By.ID, "lastName"))).send_keys(last_name)
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(password)
        wait.until(EC.presence_of_element_located((By.NAME, "ConfirmPasswd"))).send_keys(password)

        # Click "Next" button
        wait.until(EC.element_to_be_clickable((By.ID, "accountDetailsNext"))).click()

        logging.info(f"Successfully created account: {email}")
        save_account(email, proxy)

    except Exception as e:
        logging.error(f"Error creating account: {e}")

    finally:
        if driver:  # Ensure driver is defined before quitting
            driver.quit()

# Main Execution
if __name__ == "__main__":
    num_accounts = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    # User must enter password manually
    password = input("Enter a password for all accounts: ")
    if len(password) < 6:
        print("Password must be at least 6 characters!")
        sys.exit(1)

    for _ in range(num_accounts):
        create_gmail_account(password)
        time.sleep(random.uniform(7.5, 15.0))  # More variability to avoid detection