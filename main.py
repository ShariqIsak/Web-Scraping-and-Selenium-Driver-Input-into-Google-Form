from bs4 import BeautifulSoup
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Inspired by Day 63 of Angela Yu's, 100 Days of Code Python Bootcamp - This project scraps data from a property
# website (BuyRentKenya) using BeautifulSoup and then inputs them into a Google form using Selenium webdriver
# Code is working as at 30 Nov 2023


# Links to the property website and google form set here
PROPERTY_WEBSITE = "https://www.buyrentkenya.com/houses-for-rent/nairobi/westlands?price=0-100000"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLScbEikdLfCMWwFRAuGqRE_wyVSULEn6vjlydSA2Kaz2Mbh76Q/viewform"

response = requests.get(PROPERTY_WEBSITE)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

# Scrape the website for the all the house descriptions, prices and links to the properties

houses = soup.findAll(name="span", class_="relative top-[2px] hidden md:inline")
prices = soup.findAll(name="a", class_="no-underline")
links = soup.findAll(name="a", class_="text-black no-underline", href=True)


# Create lists to add the the found data
house_list = []
price_list = []
link_list = []

# Scrape for Prices
for a in range(2, 21):
    # Skip the adverts on the page
    if a == 4 or a == 13 or a == 19 or a == 20:
        pass
    else:
        # Convert the BeautifulSoup file to etree for XPATH searching and create a list of objects
        xpath_str = f"/html/body/div[1]/div/div/div[4]/div[1]/div[1]/div/div[1]/div[3]/div/div[2]/div/div[1]/div/span/div[{a}]/div/div/div[2]/div[2]/div[1]/div[1]/p/a"
        body = soup.find("body")
        dom = etree.HTML(str(body))
        price_list.append(dom.xpath(xpath_str)[0].text.split('\n')[1])

# Append to link_list all property website links
for a in range(len(links)):
    link_list.append(links[a]['href'])

# Initialize the chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM)


# Loop through each listing on page 1 of results and then input to the google form
for a in range(len(houses)):
    # Append the house title to house_list
    house_list.append(houses[a].getText().split("\n")[1])
    # Printing variables here to check for errors
    print(a)
    print(house_list[a])
    print(price_list[a])
    print(link_list[a])

    time.sleep(3)

    # Input the Name, Price and Link on to the google form

    location_input = driver.find_element(By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    location_input.send_keys(house_list[a])

    price_input = driver.find_element(By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(price_list[a])

    link_input = driver.find_element(By.XPATH, value='/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(link_list[a])

    submit_button = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
    submit_button.click()

    time.sleep(3)

    submit_again_button = driver.find_element(By.XPATH, value="/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
    submit_again_button.click()
