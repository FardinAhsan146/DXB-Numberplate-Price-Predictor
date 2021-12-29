import time
import re
import requests 
import numpy as np
import pandas as pd
import concurrent.futures

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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
SCROLL_PAUSE_TIME = 1
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
        time.sleep(SCROLL_PAUSE_TIME)

        # Exit clause if end of page is reached
        new_height = driver.execute_script(height_script)
        if new_height == last_height:
            break
        last_height = new_height
    
    # Break out if button doesn't work
    # It should so this is in case of error
    except ElementNotInteractableException:
        break


# Find the html blocks we need for the number plates
border_selector = '.bntborder.padding-single'
plate_borders = driver.find_elements_by_css_selector(border_selector)



# Create a threadpool executor to speed up the i/o requests
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []       # List to hold the future objects
    for elem in plate_borders:
        futures.append(
            executor.submit(
                lambda elem: elem.get_attribute("innerHTML"),
                elem = elem
            )
        )
    
    # Html elements of the border we chose by css selector
    border_htmls =\
    [future.result() for future in concurrent.futures.as_completed(futures)]

#Close driver for good!
driver.quit()

# Create lists to put in data we need
code_list = []
number_list = []
price_list = []
city_list = []

for html_element in border_htmls:
    #Creatre soup obejct
    soup = BeautifulSoup(html_element, 'html.parser')
    
    # Find the code
    code_regex = re.compile('.*plate_code.*')
    code = soup.find('div', {"class" : code_regex}).text
    code_list.append(code)
    
    # Find number
    number_regex = re.compile('.*plate_nub.*')
    number = soup.find('div', {"class" : number_regex}).text
    number_list.append(number)
    
    # Price
    price = soup.find('span', {"class" : 'txt24bld pricered text-center'}).text
    price_list.append(price)
    
    #city 
    img_str = str(soup.find('div', {"class" : 'plate_img'}))
    img_regex = re.compile("images/(.*?)\.svg")
    city = re.findall(img_regex,img_str)[0]
    city_list.append(city)

# Create the dataframe
df = pd.DataFrame({
    'code':code_list,
    'number':number_list,
    'price':price_list,
    'city':city_list,
})

# Remove new lines from price
# So that it shows up in csv
df['price'] = df['price'].replace('\n','', regex = True)

#Save as a csv
df.to_csv('datasets/scraped.csv', index = False)