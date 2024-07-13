from modules import *
import json
import time

# Initialize the Selenium WebDriver

# Open the webpage
driver.get('https://www.zomato.com/ncr/karol-bagh-delhi-restaurants')  # Replace with the actual URL

# Wait for the page to load
time.sleep(3)

# Function to scroll down the page slowly
def scroll_down_page(driver, speed=45):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        time.sleep(0.1)
        new_height = driver.execute_script("return document.body.scrollHeight")

# Scroll down the page slowly
scroll_down_page(driver)

# Wait for the elements to load
driver.implicitly_wait(10)

# Find all card elements
cards = driver.find_elements(By.CLASS_NAME, 'sc-imAxmJ')

# Extract the href links from the a tags within each card
links = []
for card in cards:
    try:
        link_element = card.find_element(By.TAG_NAME, 'a')
        href = link_element.get_attribute('href')
        links.append(href)
    except Exception as e:
        print(f"Error extracting link from card: {e}")

# Save the links in a JSON file
data = {"links": links}

with open('links.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Close the browser
driver.quit()
