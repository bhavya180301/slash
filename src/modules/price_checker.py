from src.modules.product_url_scraper import product_price_google,product_price_amazon,product_price_bjs

def check_price_drop(product_url,product_price,product_website):
    """
    Checks if the price of a product has dropped based on the provided product URL,
    current product price, and the website where the product is listed.

    Parameters:
    - product_url (str): The URL of the product.
    - product_price (str): The current price of the product.
    - product_website (str): The website where the product is listed (e.g., 'bjs', 'google', 'amazon').

    Returns:
    - str: Returns 'true' if the price has dropped, 'false' otherwise.
    """
    
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

