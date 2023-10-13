from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from scraper import driver

app = Flask(__name__, template_folder=".")
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
db=SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=50),nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)



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