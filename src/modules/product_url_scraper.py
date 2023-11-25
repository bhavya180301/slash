from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)




def product_price_bjs(product_url):
    driver.get(product_url)
    elements = driver.find_elements(By.CLASS_NAME, 'cls-price')
    return elements[1].text

def product_price_google(product_url):
    driver.get(product_url)
    elements = driver.find_elements(By.CLASS_NAME,'g9WBQb')
    return elements[0].text

def product_price_amazon(product_url):
    driver.get(product_url)
    elements = driver.find_elements(By.CLASS_NAME,'a-price-whole')
    return elements[0].text

