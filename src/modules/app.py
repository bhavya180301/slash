from webapp import app
from flask import request,render_template
from scraper import driver
from webapp.forms import RegisterForm
@app.route("/")
def landingpage():
    return render_template("./static/landing.html")


@app.route("/search", methods=["POST", "GET"])
def product_search(new_product="", sort=None, currency=None, num=None):
    product = request.args.get("product_name")
    if product == None:
        product = new_product

    data = driver(product, currency, num, 0, False, None, True, sort)

    return render_template("./static/result.html", data=data, prod=product)


@app.route("/filter", methods=["POST", "GET"])
def product_search_filtered():

    product = request.args.get("product_name")
    sort = request.form["sort"]
    currency = request.form["currency"]
    num = request.form["num"]

    if sort == "default":
        sort = None
    if currency == "usd":
        currency = None
    if num == "default":
        num = None
    return product_search(product, sort, currency, num)

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template("./static/register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)

