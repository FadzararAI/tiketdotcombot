import pickle
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# Browser initialization
chrome_options = Options()
chrome_options.add_argument("--log-level=3");
#chrome_options.add_argument("--headless");
driver = webdriver.Chrome(options=chrome_options,executable_path="webdriver/chromedriver.exe")
driver.implicitly_wait(10)

# Ticket link (tiket.com)
driver.get("https://www.tiket.com/to-do/viu-scream-dates")

#Cookies loader (Log-in)
cookies = pickle.load(open("cookies.pkl","rb"))
for cookie in cookies:
	driver.add_cookie(cookie)
driver.refresh()

# Ticket prices extractor
def prod_pricelist(tickets):
	global soup
	soup = BeautifulSoup(tickets,'html.parser')
	global product_names
	product_names = ['',]
	global product_prices
	product_prices = ['',]
	global sold_out
	sold_out = ['',]
	for i in soup.find_all('h3',{'class': 'PackageSelection_package_title__IxGiM'}):
		product_names.append(i.get_text())
	for i in soup.find_all('div',{'class': 'PackageSelection_package_price__93cz_'}):
		product_prices.append(i.get_text())
	for i in soup.find_all('h3',{'class': 'HcPVsG_variant_disabled'}):
		sold_out.append(i.get_text())
	print("=========== PRICE LIST ===============")
	if len(sold_out) != 1:
		for i in range(len(sold_out)):
			if i == 0:
				continue
			print(str(i)+ '. ' + str(product_names[i]) + " : " + str(product_prices[i]))
	elif len(sold_out) == 1:
		for i in range(len(product_names)):
			if i == 0:
				continue
			print(str(i)+ '. ' + str(product_names[i]) + " : " + str(product_prices[i]))

# Checker if there are many tickets
try:
	driver.find_element(By.XPATH, "//button[contains(text(),'Tampilkan')]").click()
	sources = driver.page_source
	prod_pricelist(sources)
except:
	sources = driver.page_source
	prod_pricelist(sources)
pilih_tiket = int(input("Pilih Tiket: "))

pilih_tiket = 1
# Ticket selector
actions = ActionChains(driver)
tiket = driver.find_element(By.XPATH,f"(//button[contains(text(),'Pilih Tiket')])[{pilih_tiket}]")
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",tiket)
tiket.click()

# Automatically adds 2 people in the ticket
driver.find_element(By.XPATH, "(//button[@class='ZfMCoW_operation_button'])[2]").click()
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Automatically checked 'sama dengan pemesan'
psng = driver.find_element(By.XPATH, '(//button)[3]')
bayar = driver.find_element(By.XPATH, "(//button)[4]")
actions.move_to_element(bayar).perform()
psng.click()
driver.execute_script("arguments[0].scrollIntoView();", bayar)

#driver.save_screenshot('END.png')
# Check-out. Uncomment to enable check-out process
#bayar.click()
time.sleep(10)
