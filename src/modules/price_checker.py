from flask import Flask, request, render_template, send_file, make_response,jsonify
from src.modules.scraper import driver

def check_price_drop(product_name,product_price):
    print("Checking Price!!")
    results = driver(product_name,"")
    json_data = results.to_dict(orient='records')
    for res in json_data:
        if(res['title'] == product_name):
            product = res
            break
        else : 
            product=None
    product_price_new = float(product['price'].replace("$", ""))
    product_price = float(product_price.replace("$", ""))
    print(product['title'])
    print(product_price)
    print(product_price_new)
    
    if(product_price_new >= product_price):
        print("false")
        return jsonify("false")
    print("true")
    return jsonify("true")

