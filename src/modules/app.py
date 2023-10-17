from datetime import datetime

from flask import Flask, request, render_template, send_file, make_response
from src.modules.csv_writer import write_csv

from src.modules.scraper import driver
import pandas as pd
import pdfkit

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

app = Flask(__name__, template_folder=".")


@app.route("/")
def landingpage():
    return render_template("./static/landing.html")


@app.route("/search", methods=["POST", "GET"])
def product_search(new_product="", sort=None, currency=None, num=None, csv=None):
    product = request.args.get("product_name")
    if product is None:
        product = new_product

    data = driver(product, currency, num, 0, None, None, True, sort)

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


@app.route("/csv", methods=["POST", "GET"])
def csv_maker():
    product = request.args.get("product_name")
    data = driver(product, None, None, 0, None, None, True)
    file_name = write_csv(data, product, r'C:\Users\smith\Desktop\NCSU-SEM-1\SE\slash\src\csvs')

    return send_file(fr'C:\Users\smith\Desktop\NCSU-SEM-1\SE\slash\src\csvs\{file_name}', as_attachment=True)


@app.route("/pdf", methods=["POST", "GET"])
def pdf_maker():
    product = request.args.get("product_name")
    now = datetime.now()
    data = driver(product, None, None, 0, None, None, True)
    html_table = render_template("./static/pdf_maker.html", data=data, prod=product)
    options = {
        'page-size': 'A4',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        'debug-javascript': None,
        'no-images': None,
        "enable-local-file-access": "",
    }

    pdfkit.from_string(html_table,
                       fr'C:\Users\smith\Desktop\NCSU-SEM-1\SE\slash\src\pdfs\{product + now.strftime("%m%d%y_%H%M")}.pdf',
                       configuration=config,
                       options=options)
    return send_file(
        fr'C:\Users\smith\Desktop\NCSU-SEM-1\SE\slash\src\pdfs\{product + now.strftime("%m%d%y_%H%M")}.pdf',
        as_attachment=True)
