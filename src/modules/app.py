from datetime import datetime

from flask import Flask, request, render_template, send_file, make_response,jsonify
from src.modules.csv_writer import write_csv
from apscheduler.schedulers.background import BackgroundScheduler
from src.modules.scraper import driver
from src.modules.data import categories
from src.modules.data import category_images
import pandas as pd
import pdfkit
from src.modules.product_url_scraper import product_price_bjs, product_price_google, product_price_amazon
from src.modules.price_checker import check_price_drop
path_wkhtmltopdf = "src/modules/wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, template_folder=".")


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'seproject37@gmail.com'
app.config['MAIL_PASSWORD'] = 'ffyi cwen stql peyj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '504038774627ae2489c38028'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
scheduler = BackgroundScheduler()
scheduler.start()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)

    @property
    def passwordInput(self):
        return self.passwordInput

    @passwordInput.setter
    def passwordInput(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class Wishlist(db.Model):

    id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer(),db.ForeignKey('users.id'))
    product_title=db.Column(db.String(length=1000),nullable=False)
    product_link=db.Column(db.String(length=1000),nullable=False)
    product_price=db.Column(db.Float(),nullable=True)
    product_website=db.Column(db.String(length=100),nullable=False)
    product_image_url=db.Column(db.String(length=10000),nullable=False)
    product_rating=db.Column(db.String(length=10),nullable=True)



@app.route("/")
def landingpage():
    data = category_images
    return render_template("./webapp/static/landing.html", data=data)

@app.route("/checkpricedrop", methods=["POST"])
def checkpricedrop():
    product_url = request.form.get("product_url")
    product_price = request.form.get("product_price")
    product_website = request.form.get("product_website")
    if(product_website == 'bjs') :
        product_price_new = product_price_bjs(product_url)

    if(product_website == 'google'):
        product_price_new = product_price_google(product_url)

    if(product_website == 'amazon'):
        product_price_new = product_price_amazon(product_url)
   
    product_price_new = float(product_price_new.replace("$", ""))
    product_price = float(product_price.replace("$", ""))
    
    if(product_price_new >= product_price):
        return jsonify("false")
    
    return jsonify("true")

job_registry = {}

def scheduled_price_check(**kwargs):
    with app.app_context():
        price_drop = check_price_drop(kwargs['product_url'],kwargs['product_price'],kwargs['product_website'])
        email = kwargs['email']
        print(price_drop)
        if price_drop == "true" : 
            msg = Message('Price Drop Alert', sender = 'seproject37@gmail.com', recipients = [email])
            msg.body= "New Price Drop recorded in " + kwargs['product_url']
            mail.send(msg)
        


@app.route('/set_price_alert', methods=['POST'])
def initiate_price_check():
    product_url = request.form.get('product_url')
    product_price = request.form.get('product_price')
    email = request.form.get('email')
    product_website = request.form.get('product_website')

    
    # Add the job to the scheduler with parameters
    with app.app_context():
        job = scheduler.add_job(scheduled_price_check, 'interval', minutes=0.5,
                  kwargs={'product_url': product_url,'product_price':product_price,'email':email,'product_website':product_website})
        job_registry[product_url] = job


    return jsonify('Price drop check initiated!')

@app.route('/stop_price_alert', methods=['POST'])
def stop_price_check():
    # Retrieve the job from the registry based on the product URL
    product_url = request.form.get('product_url')
    job = job_registry.get(product_url)

    if job:
        try:
            # Remove the job from the scheduler
            scheduler.remove_job(job.id)
            del job_registry[product_url]
            return jsonify({'status': 'success', 'message': 'Price check stopped successfully'})
        except :
            return jsonify({'status': 'error', 'message': 'Job not found in the scheduler'})
    else:
        return jsonify({'status': 'error', 'message': 'Job not found in the registry'})


@app.route("/category/<category_query>", methods=["GET"])
def category_result(category_query):
    data = categories[category_query]
    return render_template("./webapp/static/category_result.html", data=data)


@app.route("/search", methods=["POST", "GET"])
def product_search(new_product="", sort=None, currency=None, num=None, filter_by_rating=None, csv=None, websites=None):
    product = request.args.get("product_name")
    if product is None:
        product = new_product

    data = driver(product, currency, num, 0, None, None, True, sort, filter_by_rating,websites)

    return render_template("./webapp/static/result.html", data=data, prod=product, currency=currency, sort=sort, num=num, user_login=current_user.is_authenticated,websites=websites)


@app.route("/filter", methods=["POST", "GET"])
def product_search_filtered():
    product = request.args.get("product_name")

    websites=[]
    sort = request.form["sort"]
    currency = request.form["currency"]
    num = request.form["num"]
    filter_by_rating = request.form["filter-by-rating"]

    if sort == "default":
        sort = None
    if currency == "usd":
        currency = None
    if num == "default":
        num = None
    if filter_by_rating == "default":
        filter_by_rating = None
    
    if "filter-search" in request.form:
        print("Filter Search Detected and Websites found")
        amazon=-1
        walmart=-1
        etsy=-1
        bj=-1
        google=-1
        print(request.form)
        amazon=request.form.get("amazon")
        print(amazon)
        etsy=request.form.get("etsy")
        print(etsy)
        walmart=request.form.get("walmart")
        print(walmart)
        bj=request.form.get("bj")
        print(bj)
        google=request.form.get("google")
        print(google)
        if amazon!=-1:
            websites.append(amazon)
        if walmart!=-1:
            websites.append(walmart)
        if google!=-1:
            websites.append(google)
        if bj!=-1:
            websites.append(bj)
        if etsy!=-1:
            websites.append(etsy)
        return product_search(product, sort, currency, num, filter_by_rating, None, websites)
      
    elif "convert-to-csv" in request.form:

        data = driver(product, currency, num, 0, None, None, True, sort, filter_by_rating)

        file_name = write_csv(data, product, "./src/modules/csvs")

        return send_file(f"./csvs/{file_name}", as_attachment=True)


    elif "convert-to-pdf" in request.form:
        now = datetime.now()
        data = driver(product, currency, num, 0, None, None, True, sort, filter_by_rating,websites)
        html_table = render_template("./webapp/static/pdf_maker.html", data=data, prod=product)
        file_name = product + now.strftime("%m%d%y_%H%M") + '.pdf'

        pdfkit.from_string(html_table,
                           f"./src/modules/pdfs/{file_name}",
                           configuration=config,
                           options={"enable-local-file-access": ""})
        return send_file(
            f"./pdfs/{file_name}",
            as_attachment=True)

@app.route("/add-to-wishlist", methods=["POST", "GET"])
def add_to_wishlist():
    # Retrieve user ID from the session

    

    # Retrieve product details from the request JSON
    product_title = request.json.get("product_title")
    product_link = request.json.get("product_link")
    product_price = request.json.get("product_price")[1:]
    product_website = request.json.get("product_website")
    product_rating = request.json.get("product_rating")
    product_image_url = request.json.get("product_image_url")

    

    # Assuming you have a Wishlist model
    wishlist_product = Wishlist(
        user_id=current_user.id,
        product_title=product_title,
        product_link=product_link,
        product_price=float(product_price),
        product_website=product_website,
        product_rating=product_rating,
        product_image_url=product_image_url
    )

    db.session.add(wishlist_product)
    db.session.commit()
    

    return "true"


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    from src.modules.forms import RegisterForm
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user_to_create = Users(name=form.name.data,
                                   email=form.email.data,
                                   passwordInput=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            flash('Registered successfully! Login to create wishlists', category='success')
            return redirect(url_for('landingpage'))
        except IntegrityError:
            db.session.rollback()
            flash('An account with this email already exists. Please use a different email.', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user: {err_msg}', category='danger')
    return render_template("./webapp/static/register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():

    from src.modules.forms import LoginForm
    form=LoginForm()

    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.email} ', category='success')
            return redirect(url_for('landingpage'))

        else:
            flash('Email or password do not match! Please try again', category='danger')

    return render_template("./webapp/static/login.html", form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('landingpage'))


@app.route("/wishlist", methods=['GET'])
def wishlist():
    if current_user.is_authenticated:
        wishlists = Wishlist.query.filter_by(user_id=current_user.id).all()
        return render_template("./webapp/static/wishlist.html", user=current_user.id, data=wishlists)
    return login_page()
