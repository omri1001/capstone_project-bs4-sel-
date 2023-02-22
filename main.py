from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


list_of_links = []
list_of_addresses = []
list_of_prices = []


forms_url = "https://docs.google.com/forms/d/e/1FAIpQLSfxKruako4EedvxAFzsAQroqt7CMfTLv_RxJMC2J5cgMNc7rg/viewform?usp=sf_link"
zillow_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
response = requests.get(zillow_url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36", "Accept-Language":"en-US"})
soup = BeautifulSoup(response.text, "html.parser")

list_of_apartments = soup.find(class_="result-list-container").find(name="ul").findAll(name="li")

#pprint(list_of_apartments)


for apartment in list_of_apartments:
    card = apartment.find(class_="property-card-data")
    try:
        link = apartment.find(name="a").get('href')
        address = apartment.find(name="a").text
        if "https" not in link:
            link = 'https://www.zillow.com' + link
        list_of_links.append(link)
        list_of_addresses.append(address)
    except:
        pass

    try:
        price = apartment.find(class_="gugdBn").find(name="span").text
        list_of_prices.append(price)
    except:
        pass

print(list_of_links)
print(list_of_prices)
print(list_of_addresses)


chrome_driver_path = "C:\development\chromedriver"


for n in range(len(list_of_links)):
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(forms_url)
    time.sleep(10)
    address_answer = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(1) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
    address_answer.send_keys(list_of_addresses[n])
    price_answer = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(2) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
    price_answer.send_keys(list_of_prices[n])
    link_answer = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.o3Dpx > div:nth-child(3) > div > div > div.AgroKb > div > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
    link_answer.send_keys(list_of_links[n])
    submit_button = driver.find_element(By.CSS_SELECTOR, "#mG61Hd > div.RH5hzf.RLS9Fe > div > div.ThHDze > div.DE3NNc.CekdCb > div.lRwqcd > div > span")
    submit_button.click()
    driver.quit()
    time.sleep(3)


