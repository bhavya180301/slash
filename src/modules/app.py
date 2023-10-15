from webapp import app, db
from flask import request, render_template, redirect, url_for
from scraper import driver
from webapp.forms import RegisterForm
from src.modules.webapp.models import Users
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

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create=Users(name=form.name.data,
                             email=form.email.data,
                             password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('landingpage'))
    return render_template("./static/register.html", form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        user1 = Users(name="Yash", email="y@yahhoo.com", password="1234")
        db.session.add(user1)
        db.session.commit()


        users = Users.query.all()
        print(users)
    app.run(debug=True)

