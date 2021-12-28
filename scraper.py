import time
import numpy as np
import pandas as pd

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException 

# Webdriver settings
options = Options()
driver_manager = ChromeDriverManager().install()
driver = webdriver.Chrome(driver_manager,
                          options=options)

# Open website
driver.implicitly_wait(5)
driver.get('https://plates.ae/plate.php')

# Infinite scroll down to the bottom of the website
scroll_pause_time = 1
height_script = "return document.body.scrollHeight"
last_height = driver.execute_script(height_script)
while True:

    try:
        script = 'window.scrollTo(0, document.body.scrollHeight);'
        element_xpath = "//button[contains(text(), 'مشاهدة المزيد من اللوحات')]"

        # Scroll to the bottom of the page
        driver.execute_script(script)

        # Click the button at the end of the page
        driver.find_elements_by_xpath(element_xpath)[0].click()
        time.sleep(scroll_pause_time)

        # Exit clause if end of page is reached
        new_height = driver.execute_script(height_script)
        if new_height == last_height:
            break
        last_height = new_height

    except ElementNotInteractableException:
        break

# Extract data needed from webpage 
number_css = '.plate_nub.one_db.dubai_font1.web_dbnum_on'
letter_css = '.plate_code.one_db.dubai_font1.db_one.web_dbcode_on'
price_css =  '.txt24bld.pricered.text-center'

number = driver.find_elements_by_css_selector(number_css)
letter = driver.find_elements_by_css_selector(letter_css)
price  = driver.find_elements_by_css_selector(price_css)
# Create csv
# df = pd.DataFrame()
# df['number'] = np.array([n.text for n in number])
# df['letter'] = np.array([l.text for l in letter])
# df['price'] = np.array([p.text for p in price])

# df.to_csv('datasets/plates.csv')

for i in range(100):
    print(number[i].text,letter[i].text,price[i].text)

driver.quit()