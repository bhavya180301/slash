from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)




def product_price_bjs(product_url):
    """
    Fetches the product price from the provided BJ's Wholesale Club product URL.

    Parameters:
    - product_url (str): The URL of the product on BJ's Wholesale Club.

    Returns:
    - str: The product price.
    """

    driver.get(product_url)
    elements = driver.find_elements(By.CLASS_NAME, 'cls-price')
    return elements[1].text

def product_price_google(product_url):
    """
    Fetches the product price from the provided Google Shopping product URL.

    Parameters:
    - product_url (str): The URL of the product on Google Shopping.

    Returns:
    - str: The product price.
    """
    driver.get(product_url)
    elements = driver.find_elements(By.CLASS_NAME,'g9WBQb')
    return elements[0].text

def product_price_amazon(product_url):
    """
    Fetches the product price from the provided Amazon product URL.

    Parameters:
    - product_url (str): The URL of the product on Amazon.

    Returns:
    - str: The product price.
    """
    driver.get(product_url)
    elements = driver.find_elements(By.CLASS_NAME,'a-price-whole')
    return elements[0].text

