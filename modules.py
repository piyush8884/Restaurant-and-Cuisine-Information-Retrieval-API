import os
from itertools import chain
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.common.action_chains import ActionChains
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
import time
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

List_of_all = []
options = Options()

options.add_argument("--start-fullscreen")

#driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

List_of_all = []
options = Options()
# options.add_argument("--window-size=1920x1080")
options.add_argument("--start-fullscreen")
# options.add_argument("--verbose")
#options.add_argument("--headless")
options = webdriver.ChromeOptions()
# Set options if needed
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)