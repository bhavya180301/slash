import json
from unittest.mock import patch
import pytest
import sys
from src.modules.app import app, scheduled_price_check
from src.modules.app import Users, db, Wishlist
from flask_login import current_user, login_user
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'  # Use a test database
    app.config['WTF_CSRF_ENABLED'] = False 
    client = app.test_client()
    with app.app_context():
        db.create_all()  # Create the test database
        test_user = Users(name='Test User', email='test@example.com', password='testpassword')
        db.session.add(test_user)
        db.session.commit()

        yield client
        db.session.remove()
        db.drop_all()  # Clean up the test database
    

def test_database_connection(client):
    # Test the database connection by adding a sample user
    user = Users(name='John', email='john@example.com', passwordInput='password123')
    db.session.add(user)
    db.session.commit()

    # Retrieve the user from the test database
    retrieved_user = Users.query.filter_by(email='john@example.com').first()
    assert retrieved_user is not None

def test_wishlist_database_connection(client):
    # Test the database connection by adding a sample wishlist item
    wishlist_item = Wishlist(
        user_id=1,  # Assuming there's a user with ID 1 in your test database
        product_title='Test Product',
        product_link='http://example.com/product',
        product_price=19.99,
        product_website='Example Website',
        product_rating=4.5,
        product_image_url='http://example.com/product/image.jpg'
    )
    db.session.add(wishlist_item)
    db.session.commit()

    retrieved_wishlist_item = Wishlist.query.filter_by(product_title='Test Product').first()
    assert retrieved_wishlist_item is not None


def test_user_registration(client):
    print("-------------------------------")
    print(sys.path)
    print("-------------------------------")
    # Test user registration logic
    response = client.post('/register', data=dict(
        name='NewUser',
        email='newuser@example.com',
        password1='newpassword',
        password2='newpassword'
    ), follow_redirects=True)

    # Check if the registration was successful by looking for a flash message
    assert b'Registered successfully! Login to create wishlists' in response.data

def test_user_login(client):
    # Test user login logic
    response = client.post('/register', data=dict(
        name='NewUser',
        email='newuser@example.com',
        password1='newpassword',
        password2='newpassword'
    ), follow_redirects=True)

    response = client.post('/login', data=dict(
        email='newuser@example.com',
        password='newpassword'
    ), follow_redirects=True)

    # Check if the login was successful by looking for a flash message
    assert b'Success! You are logged in as: newuser@example.com' in response.data

def test_user_logout(client):
    # Test user logout logic
    response = client.get('/logout', follow_redirects=True)

    assert b'You have been logged out!' in response.data

def test_user_registration_existing_email(client):
    # Test user registration with an existing email address
    existing_user = Users(name='Existing User', email='test2@example.com', password='existingpassword')
    db.session.add(existing_user)
    db.session.commit()

    # Simulate a registration attempt with a duplicate email
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'test2@example.com',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }, follow_redirects=True)

    
    print(response.data)
    

    # Check if the registration fails with an error message
    assert b'Email address is already in use.' in response.data

def test_user_login_invalid_credentials(client):
    # Test user login with invalid credentials
    response = client.post('/login', data=dict(
        email='nonexistent@example.com',  # Use an email that doesn't exist
        password='invalidpassword'
    ), follow_redirects=True)

    # Check if the login fails with an error message
    assert b'Email or password do not match! Please try again' in response.data



def test_add_to_wishlist(client):
    # Define the request data
    test_user = Users.query.first()
    with app.test_request_context():
        login_user(test_user)
        request_data = {
            "user_id" : current_user.id,
            "product_title": "Test Product",
            "product_link": "http://example.com/product",
            "product_price": "$19.99",
            "product_website": "Example Website",
            "product_rating": '4.5',
            "product_image_url": "http://example.com/product/image.jpg"
        }

        # Make a POST request to add the product to the wishlist
        response = client.post('/add-to-wishlist', json=request_data, content_type='application/json')
        print(response.data)
        # Check if the response is as expected


        # Check if the product is added to the database
        wishlist_product = Wishlist.query.first()
        
        assert wishlist_product.user_id == test_user.id 
        assert wishlist_product.product_title == "Test Product"
        assert wishlist_product.product_link == "http://example.com/product"
        assert wishlist_product.product_price == 19.99
        assert wishlist_product.product_website == "Example Website"
        assert wishlist_product.product_rating == '4.5'
        assert wishlist_product.product_image_url == "http://example.com/product/image.jpg"

        
def test_checkpricedrop_bjs(client):
    def mock_function(product_url):
        return "$15"
    with patch('src.modules.app.product_price_bjs',mock_function):
        
        
        response = client.post('/checkpricedrop', data=dict(
            product_url="http://example.com/product",
            product_price="$20.00",
            product_website="bjs"
        ))

        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True)) == "true"

def test_checkpricedrop_google(client):
    def mock_function(product_url):
        return "$25"
    with patch('src.modules.app.product_price_google',mock_function):
        
        
        response = client.post('/checkpricedrop', data=dict(
            product_url="http://example.com/product",
            product_price="$30.00",
            product_website="google"
        ))

        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True)) == "true"

def test_checkpricedrop_amazon(client):
    def mock_function(product_url):
        return "$45"
    
    with patch("src.modules.app.product_price_amazon",mock_function):
        
        
        response = client.post('/checkpricedrop', data=dict(
            product_url="http://example.com/product",
            product_price="$50.00",
            product_website="amazon"
        ))

        assert response.status_code == 200
        assert json.loads(response.get_data(as_text=True)) == "true"


def test_initiate_price_check(client):
    # Replace this with actual test data
    test_data = {
        'product_url': 'http://example.com/product',
        'product_price': '19.99',
        'email': 'test@example.com',
        'product_website': 'example_website'
    }

    # Use patch to mock the scheduler.add_job function
    with patch('src.modules.app.scheduler.add_job') as mock_add_job:
        # Simulate a POST request to the /set_price_alert endpoint
        response = client.post('/set_price_alert', data=test_data, follow_redirects=True)

        # Add assertions based on the expected behavior of your application
        assert response.status_code == 200
        assert mock_add_job.called
        assert mock_add_job.call_args[1]['kwargs'] == test_data



def test_stop_price_check(client):
    # Replace this with actual test data
    test_data = {
        'product_url': 'http://example.com/product'
    }

    # Use patch to mock the scheduler.remove_job function
    with patch('src.modules.app.scheduler.remove_job') as mock_remove_job:
        # Simulate a POST request to the /stop_price_alert endpoint
        response = client.post('/stop_price_alert', data=test_data, follow_redirects=True)

        # Add assertions based on the expected behavior of your application
        assert response.status_code == 200
        assert mock_remove_job.called
        assert mock_remove_job.call_args[0][0]  # Check if remove_job was called with at least one argument
        assert 'status' in response.get_json()
        assert 'message' in response.get_json()



def test_scheduled_price_check():
    # Replace this with actual test data
    test_data = {
        'product_url': 'http://example.com/product',
        'product_price': '19.99',
        'email': 'test@example.com',
        'product_website': 'example_website'
    }

    # Use patch to mock the check_price_drop function
    with patch('src.modules.app.check_price_drop') as mock_check_price_drop, \
         patch('src.modules.app.Message') as mock_message, \
         patch('src.modules.app.mail.send') as mock_send:
        # Mock the API call response
        mock_check_price_drop.return_value = 'true'

        # Call the scheduled_price_check function with test data
        scheduled_price_check(**test_data)

        # Add assertions based on the expected behavior of your application
        assert mock_check_price_drop.called
        assert mock_message.called
        assert mock_send.called
        