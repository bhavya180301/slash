from flask import Flask, request, render_template, send_file, make_response,jsonify
from src.modules.scraper import driver
from scraper import product_price
from product_url_scraper import product_price_google,product_price_amazon,product_price_bjs

def check_price_drop(product_url,product_price,product_website):
    print("Checking Price!!")
    

    if(product_website == 'bjs') :
        product_price_new = product_price_bjs(product_url)

    if(product_website == 'google'):
        product_price_new = product_price_google(product_url)

    if(product_website == 'amazon'):
        product_price_new = product_price_amazon(product_url)
   
    product_price_new = float(product_price_new.replace("$", ""))
    product_price = float(product_price.replace("$", ""))
    
    if(product_price_new >= product_price):
        return "false"
    
    return "true"

