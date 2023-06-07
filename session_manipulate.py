from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pickle
import time

# Browser initialization
chrome_options = Options()
chrome_options.add_argument("--log-level=3");
driver = webdriver.Chrome(options=chrome_options,executable_path="webdriver/chromedriver.exe")
driver.get("https://www.tiket.com/login?ref=https://www.tiket.com/")

# Login credentials. Fill them up with your login information!
email = ""
password = ""

# Auto-fill email and click 'Lanjutkan'
driver.find_element(By.ID, "nomor-ponsel-atau-email").send_keys(email)
driver.find_element(By.CSS_SELECTOR, ".KV-nSG_full_width").click()
time.sleep(1)

# Auto-fill password and login
driver.find_element(By.ID, "kata-sandi").send_keys(password)
driver.find_element(By.CSS_SELECTOR, ".KV-nSG_full_width").click()
otpcode = str(input("Masukkan Code OTP: "))
time.sleep(1)

# Auto-fill OTP Code
driver.find_element(By.CSS_SELECTOR, ".wEG1yq_otp_input").send_keys(otpcode)
driver.find_element(By.CSS_SELECTOR, ".wEG1yq_otp_input").send_keys(Keys.ENTER)
time.sleep(3)

# Saves logged-in cookie
pickle.dump(driver.get_cookies(),open("cookies.pkl","wb"))
