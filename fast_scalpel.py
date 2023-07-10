import pickle
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Browser initialization
chrome_options = Options()
chrome_options.add_argument("--log-level=3");
chrome_options.add_argument("--window-size=800,600")

# Inputs URL. Automatically changes www.tiket.com to m.tiket.com

#url = str(input("Enter URL: ")).replace("www","m")
url = "https://m.tiket.com/to-do/international-friendly-match-indonesia-vs-argentina"

#chrome_options.add_argument("--headless");
driver = webdriver.Chrome(options=chrome_options,executable_path="webdriver/chromedriver.exe")
driver.implicitly_wait(60)

import time

st = time.time()

# Ticket link (tiket.com)
driver.get(url)

#Cookies loader (Log-in)
cookies = pickle.load(open("cookies.pkl","rb"))
for cookie in cookies:
	driver.add_cookie(cookie)
driver.refresh()

# Ticket selector
# tampil = driver.find_element(By.XPATH, "//button[contains(text(),'Tampilkan')]")
# driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",tampil)
# tampil.click()
def check():
	tickets = driver.page_source
	soup = BeautifulSoup(tickets,'html.parser')
	if soup.find_all('div',{'class': 'PackageSelection_package_price__93cz_'})[1].get_text() == "IDR 600.000" and driver.find_element(By.XPATH,"(//button[contains(text(),'Pilih Tiket')])[1]").is_enabled() == True:
		return True
	else:
		return False
while check() == False:
	print("600RB not found..")
	driver.refresh()
	check()

print("600RB FOUND!")
# Checks if the first button "Pilih Tiket" is clickable. Refreshes every 1 second if not.
while True:
	try:
        # Wait until the button is clickable
		wait = WebDriverWait(driver, 0)
		tiket = wait.until(EC.element_to_be_clickable((By.XPATH,"(//button[contains(text(),'Pilih Tiket')])[1]")))  # Replace "myButton" with the actual ID of the button
		break
	except TimeoutException:
        # Handle when cannot order ticket, refreshes when can't.
		print("Cannot order ticket, refreshing..")
		driver.refresh()
try:
	# Automatically chooses the first (cheapest) ticket.
	driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",tiket)
	tiket.click()
	# Automatically adds 2 people in the ticket
	driver.find_element(By.XPATH, "(//button[@class='ZfMCoW_operation_button'])[2]").click()

	driver.find_element(By.XPATH, "//button[contains(text(),'Pesan')]").click()

	# Automatically checked 'sama dengan pemesan'
	actions = ActionChains(driver)
	psng = driver.find_element(By.XPATH, '(//input)')
	psng.click()
	while True:
		try:
			wait = WebDriverWait(driver, 0)
			bayar = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Lanjutkan')]")))
			actions.move_to_element(bayar).perform()
			driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",bayar)
			driver.execute_script("arguments[0].scrollIntoView();", bayar)
			break
		except TimeoutException:
			print("Coba Lagi....")
			driver.refresh()
	print('Execution time:', time.time() - st, 'seconds')
	# Check-out. Uncomment to enable check-out process
	#bayar.click()
	input("Input anything to stop program..")
except:
	input("ERROR FOUND! MANUAL MODE IS ON!")
