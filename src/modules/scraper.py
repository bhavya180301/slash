"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com
"""

"""
The scraper module holds functions that actually scrape the e-commerce websites
"""

import requests
from src.modules.formatter import formatSearchQuery, formatResult, getCurrency, sortList
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import os
from datetime import datetime

# Setting headers and scraping URL 
def httpsGet(URL):
    """
    The httpsGet function makes HTTP called to the requested URL with custom headers
    Parameters:
    - URL (str): The URL to make the HTTP request to.

    Returns:
    - BeautifulSoup: A BeautifulSoup object representing the parsed HTML content.
    """

    # Custom headers to mimic a web browser's request
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
    }

    s = requests.Session()

    # Make an HTTP GET request to the URL with custom headers
    page = s.get(URL, headers=headers) 

    soup1 = BeautifulSoup(page.content, 'html.parser')

    return BeautifulSoup(soup1.prettify(), 'html.parser')

# Scraping Amazon
def searchAmazon(query, df_flag, currency):
    """
    The searchAmazon function scrapes amazon.com
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on Amazon.com that match the product entered by the user.
    """
    query = formatSearchQuery(query)
    URL = f"https://www.amazon.com/s?k={query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"data-component-type": "s-search-result"})
    products = []
    for res in results:
        titles, prices, links = (
            res.select("h2 a span"),
            res.select("span.a-price span"),
            res.select("h2 a.a-link-normal"),
        )
        image = res.find("img", {"src": True})
   
        if image :
            image_url = image.get("src").strip()
        else :
            image_url = ""
        ratings = res.select("span.a-icon-alt")
        num_ratings = res.select("span.a-size-base")
        trending = res.select("span.a-badge-text")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None
        product = formatResult(
            "amazon",
            titles,
            prices,
            links,
            ratings,
            num_ratings,
            trending,
            df_flag,
            currency,
            image_url
        )
        products.append(product)
    print(f"Amazon products : {len(products)}")
    return products

# Scraping Walmart
def searchWalmart(query, df_flag, currency):
    """
    The searchWalmart function scrapes walmart.com
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on walmart.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    URL = f"https://www.walmart.com/search?q={query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"data-item-id": True})
    products = []
    pattern = re.compile(r"out of 5 Stars")
    for res in results:
        # Extract relevant information such as titles, prices, links, etc.
        titles, prices, links = (
            res.select("span.lh-title"),
            res.select("div.lh-copy"),
            res.select("a"),
        )

        # Extract the product image URL
        image = res.find("img", {"src": True})
   
        if image :
            image_url = image.get("src").strip()
        else :
            image_url = ""
        
        # Extract ratings information
        ratings = res.findAll("span", {"class": "w_DE"}, text=pattern)
        num_ratings = res.findAll("span", {"class": "sans-serif gray f7"})

        # Extract trending badge information
        trending = res.select("span.w_Cs")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None

        # Format the result and append to the products list
        product = formatResult(
            "walmart",
            titles,
            prices,
            links,
            ratings,
            num_ratings,
            trending,
            df_flag,
            currency,
            image_url
        )
        products.append(product)
    print(f"Walmart products : {len(products)}")
    return products

# Scraping Etsy
def searchEtsy(query, df_flag, currency):
    """
    The searchEtsy function scrapes Etsy.com
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on Etsy.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    url = f"https://www.etsy.com/search?q={query}"
    products = []
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}   
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    for item in soup.select(".wt-grid__item-xs-6"):
        # Extract the links, titles, and prices
        str = item.select("a")
        if str == []:
            continue
        else:
            links = str
        titles, prices = (item.select("h3")), (item.select(".currency-value"))

        # Extract ratings information
        ratings = item.select("span.screen-reader-only")
        num_ratings = item.select("span.wt-text-body-01")

        # Extract trending badge information
        trending = item.select("span.wt-badge")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None

        # Format the result and append to the products list
        product = formatResult(
            "Etsy",
            titles,
            prices,
            links,
            ratings,
            num_ratings,
            trending,
            df_flag,
            currency,
        )
        products.append(product)
    print(f"Etsy products : {len(products)}")
    return products

# Scraping Google
def searchGoogleShopping(query, df_flag, currency):
    """
    The searchGoogleShopping function scrapes https://shopping.google.com/
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on walmart.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    URL = f"https://www.google.com/search?tbm=shop&q={query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"class": "sh-dgr__grid-result"})
    products = []
    pattern = re.compile(r"[0-9]+ product reviews")
    for res in results:
        # Extract titles, prices, and links
        titles, prices, links = (
            res.select("h3"),
            res.select("span.a8Pemb"),
            res.select("a")
        )

        # Extract the product image URL
        image = res.find("img", {"data-image-src": True})
        if image :
            image_url = image.get("data-image-src").strip()
        else :
            image_url = ""

        # Extract ratings information
        ratings = res.findAll("span", {"class": "Rsc7Yb"})
        # Extract the number of ratings using the regex pattern
        try:
            num_ratings = pattern.findall(str(res.findAll("span")[1]))[0].replace(
                "product reviews", ""
            )
        except:
            num_ratings = 0

        # Extract trending badge information
        trending = res.select("span.Ib8pOd")
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None

        # Format the result and append to the products list
        product = formatResult(
            "google",
            titles,
            prices,
            links,
            ratings,
            int(num_ratings),
            trending,
            df_flag,
            currency,
            image_url
        )
        products.append(product)
    print(f"Google products : {len(products)}")
    
    return products

# Scraping BJ
def searchBJs(query, df_flag, currency):
    """
    The searchBJs function scrapes https://www.bjs.com/
    Parameters: query- search query for the product, df_flag- flag variable, currency- currency type entered by the user
    Returns a list of items available on walmart.com that match the product entered by the user
    """
    query = formatSearchQuery(query)
    URL = f"https://www.bjs.com/search/{query}"
    page = httpsGet(URL)
    results = page.findAll("div", {"class": "product"})
    products = []

    for res in results:
        # Extract titles, prices, and links
        titles, prices, links = (
            res.select("p.no-select.d-none.d-sm-block.auto-height"),
            res.select("span.price"),
            res.select("a"),
        )

        # Extract ratings information
        ratings = res.findAll("span", {"class": "on"})
        num_ratings = 0

         # Extract trending badge information
        trending = res.select("p.instantSavings")

        # Extract the product image URL
        image_url = res.select("img.img-link")[0].get('src')
        
        # Check if there are ratings
        if len(trending) > 0:
            trending = trending[0]
        else:
            trending = None
        
        # Format the result and append to the products list
        product = formatResult(
            "bjs", 
            titles, 
            prices, 
            links, 
            "", 
            num_ratings, 
            trending, 
            df_flag, 
            currency, 
            image_url
        )
        if len(ratings) != 0:
            product["rating"] = len(ratings)
        products.append(product)
    print(f"BJs products : {len(products)}")
    return products

# Function to limit the number of entries in result
def condense_helper(result_condensed, list, num):
    """This is a helper function to limit number of entries in the result"""
    for p in list:
        if num is not None and len(result_condensed) >= int(num):
            break
        else:
            if p["title"] != None and p["title"] != "":
                result_condensed.append(p)

# Extracting price of a product from a given URL
def product_price(product_url) :
    page = httpsGet(product_url)
    results = page.findAll("div", {"data-item-id": True})
    print(results)

# Main driver function to collect all scraped data and process it to send relevant information
def driver(
    product, currency, num=None, df_flag=0, csv=None, cd=None, ui=False, sort=None, filter_by_rating=None,websites=None
):
    """
    The driver function orchestrates the entire web scraping process.

    Parameters:
    - product (str): The search query for the product.
    - currency (str): The currency type entered by the user.
    - num (int): The number of results to display or save to CSV.
    - df_flag (int): Flag variable.
    - csv (bool): Flag to indicate whether to save results to CSV.
    - cd (str): The current directory path.
    - ui (bool): Flag to indicate whether to display results in the terminal or not.
    - sort (str): The sorting criteria for the results.
    - filter_by_rating (str): The minimum rating to filter results.
    - websites (list): List of specific websites to search.

    Returns:
    - list or str: A list of condensed results or a CSV file path depending on user input.
    """
   
    # Perform individual searches on multiple websites
    products_1 = searchAmazon(product, df_flag, currency)
    products_2 = searchWalmart(product, df_flag, currency)
    products_3 = searchEtsy(product, df_flag, currency)
    products_4 = searchGoogleShopping(product, df_flag, currency)
    products_5 = searchBJs(product, df_flag, currency)
    result_condensed = ""
    if not ui:
        # Combine results from different websites into a single DataFrame
        results = products_1 + products_2 + products_3 + products_4 + products_5
        result_condensed = (
            products_1[:num]
            + products_2[:num]
            + products_3[:num]
            + products_4[:num]
            + products_5[:num]
        )
        result_condensed = pd.DataFrame.from_dict(result_condensed, orient="columns")
        results = pd.DataFrame.from_dict(results, orient="columns")

        # Drop converted price column if currency is not specified
        if currency == "" or currency == None:
            results = results.drop(columns="converted price")
            result_condensed = result_condensed.drop(columns="converted price")

        # Check if the user wants to save results to CSV
        if csv == True:
            file_name = os.path.join(
                cd, (product + datetime.now().strftime("%y%m%d_%H%M") + ".csv")
            )
            print("CSV Saved at: ", cd)
            print("File Name:", file_name)
            results.to_csv(file_name, index=False, header=results.columns)
    else:
        result_condensed = []
        # Helper function to limit the number of entries in the result
        condense_helper(result_condensed, products_1, num)
        condense_helper(result_condensed, products_2, num)
        condense_helper(result_condensed, products_3, num)
        condense_helper(result_condensed, products_4, num)
        condense_helper(result_condensed, products_5, num)

        # Convert prices to the specified currency
        if currency != None:
            for p in result_condensed:
                p["price"] = getCurrency(currency, p["price"])

        # Additional processing based on the website
        for p in result_condensed:      
            if p["website"] == "walmart":
                cleaned_price = p["price"].replace('$', '').replace(',', '').strip()
                cleaned_price = cleaned_price.replace(' ', '')
                p["price"] = float(cleaned_price)
                p["price"] = "${:.2f}".format(p["price"])
            link = p["link"]
            if p["website"] == "Etsy":
                link = link[12:]
                p["link"] = link
            elif "http" not in link:
                link = "http://" + link
                p["link"] = link

        # Sort the results based on user input
        if sort != None:
            result_condensed = pd.DataFrame(result_condensed)
            if sort == "rades":
                result_condensed = sortList(result_condensed, "ra", False)
            elif sort == "raasc":
                result_condensed = sortList(result_condensed, "ra", True)
            elif sort == "pasc":
                result_condensed = sortList(result_condensed, "pr", False)
            else:
                result_condensed = sortList(result_condensed, "pr", True)
            result_condensed = result_condensed.to_dict(orient="records")

        # Filter the results based on user-specified rating
        if filter_by_rating != None:
            result_condensed = pd.DataFrame(result_condensed)
            result_condensed = result_condensed[result_condensed['rating']!='']
            result_condensed['rating'] = result_condensed['rating'].astype(float)
            base_rating = float(filter_by_rating)
            result_condensed = result_condensed[result_condensed['rating']>=base_rating]
            result_condensed = result_condensed.to_dict(orient="records")

        if csv:
            file_name = product + "_" + datetime.now() + ".csv"
            result_condensed = result_condensed.to_csv(
                file_name, index=False, header=results.columns
            )
            print(result_condensed)
    return result_condensed
