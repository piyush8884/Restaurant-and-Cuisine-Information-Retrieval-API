import time
import json
import datetime
from bs4 import BeautifulSoup
from modules import *


def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        urls = file.readlines()
        urls = [url.strip().strip("'") for url in urls if url.strip()]
    return urls

#Function to fetch restaurant details
def fetch_restaurant_details(url):
    driver.get(url)

    # Wait until the opening hours element is present
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[div/div/text()="Dining Ratings"]')))

    # Get the page source
    page_source = driver.page_source

    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')
    opening_hours_element = soup.select_one(".sc-dwztqd.egpIQP")

    if opening_hours_element:
        opening_hours_text = opening_hours_element.get_text(strip=True)
        open_day, closed_day, last_open_day, open_time, closed_time, operational_hours = parse_opening_hours(opening_hours_text)
    else:
        open_day, closed_day, last_open_day, open_time, closed_time, operational_hours = None, None, None, None, None, None

    # Extracting other restaurant details
    restaurant_data = {}
    restaurants = driver.find_elements(By.XPATH, '//div[contains(@class, "sc-1mo3ldo")]')
    for restaurant in restaurants:
        try:
            name = restaurant.find_element(By.XPATH, '//h1[contains(@class, "sc-7kepeu-0 sc-iSDuPN")]').text
            location = restaurant.find_element(By.XPATH, '//a[contains(@class, "sc-clNaTc vNCcy")]').text

            dining_rating = fetch_dining_rating(restaurant)
            delivery_rating = fetch_delivery_rating(restaurant)
            average_pricing = fetch_average_cost(restaurant)
            url_link = driver.current_url
            popular_cuisine = restaurant.find_element(By.XPATH, '(//p[@color="#4F4F4F" and contains(@class, "sc-1hez2tp-0")])[1]').text

            reviews = fetch_reviews()
            if not reviews:
                reviews = ["No reviews here"]

            restaurant_data = {
                "restaurant name": name,
                "Dine rating": dining_rating,
                "Delivery rating": delivery_rating,
                "location": location,
                "average pricing": average_pricing,
                "url": url_link,
                "Popular cuisine": popular_cuisine,
                "open time": open_time,
                "closed time": closed_time,
                "operational_hours": operational_hours,
                "open days": open_day,
                "close days": closed_day,
                "last open day": last_open_day,
                "operational days": 7,
                "reviews": reviews
            }
        except Exception as e:
            print(f"Error fetching details for a restaurant: {e}")

    return restaurant_data


def parse_opening_hours(opening_hours_text):
    days_hours_part = opening_hours_text.split(':')
    days_part = days_hours_part[0].replace('Opening Hours', '').strip()
    hours_part = days_hours_part[1].strip()

    # Handle multiple ranges of days
    days = days_part.split(',')
    open_day = days[0].strip()
    last_open_day = days[-1].split('-')[-1].strip()

    # Extract closed day if mentioned separately
    closed_day = None
    if 'Closed' in opening_hours_text:
        closed_day = opening_hours_text.split(':')[-1].replace('Closed', '').strip()

    # Check for "24 hours" case
    if '24 Hours' in hours_part:
        open_time = '00:00'
        closed_time = '23:59'
    else:
        # Extract times and convert them to a 24-hour format
        open_time, closed_time = hours_part.split('–')
        open_time = open_time.strip()
        closed_time = closed_time.strip()

        open_hour = str(open_time[:-2]) + str(12 if 'pm' in open_time.lower() else 0)
        closed_hour = str(closed_time[:-2]) + str(12 if 'pm' in closed_time.lower() or 'midnight' in closed_time.lower() else 0)

        if 'midnight' in closed_time.lower():
            closed_hour = 24

    operational_hours = 0

    return open_day, closed_day, last_open_day, open_time, closed_time, f"{operational_hours} hours"



def fetch_dining_rating(restaurant_element):
    try:
        dining_rating_element = restaurant_element.find_element(By.XPATH,
                                                                "(//div[@class='sc-1q7bklc-1 cILgox'])[position() = 1]")
        return dining_rating_element.text.strip()
    except Exception as e:
        print(f"Error fetching dining rating: {e}")
        return None

def fetch_delivery_rating(restaurant_element):
    try:
        delivery_rating_element = restaurant_element.find_element(By.XPATH,
                                                                  "(//div[@class='sc-1q7bklc-1 cILgox'])[position() = 2]")
        return delivery_rating_element.text.strip()
    except Exception as e:
        print(f"Error fetching delivery rating: {e}")
        return None

def fetch_average_cost(restaurant_element):
    try:
        cost_element = restaurant_element.find_element(By.XPATH,
                                                       "//p[contains(text(), 'for two people (approx.)') and contains(text(), '₹')]")
        cost_text = cost_element.text
        cost_value = cost_text.split('₹')[1].split(' ')[0].replace(',', '')
        cost_value = int(cost_value)
        return cost_value
    except Exception as e:
        print(f"Error fetching average cost: {e}")
        return None


def fetch_reviews():
    try:
        reviews_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//h2[a[text()='Reviews']]")))
        time.sleep(0.5)
        reviews_link.click()
        time.sleep(0.5)

        wait = WebDriverWait(driver, 10)
        reviews = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//p[contains(@class, 'sc-1hez2tp-0') and contains(@class, 'sc-fxMfqs') and contains(@class, 'jBfxuu')]")))
        time.sleep(0.5)
        reviews_text = [review.text.strip() for review in reviews if review.text.strip()]
        return reviews_text
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return ["No reviews here"]


# Main script execution
urls = read_urls_from_file('file.txt')
all_restaurant_data = []

for url in urls:
    try:
        restaurant_data = fetch_restaurant_details(url)
        all_restaurant_data.append(restaurant_data)

        # Save data to JSON file after processing each URL
        with open('restaurant_data_rest.json', 'w') as json_file:
            json.dump(all_restaurant_data, json_file, indent=4)
        print(f"Data for {url} saved to restaurant_data_rest.json")
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

print("All data saved to restaurant_data.json")

# Close the browser
driver.quit()

