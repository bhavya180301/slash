
from unittest.mock import patch
import pytest
from src.modules.price_checker import check_price_drop

#defining mock fucntions.

@pytest.fixture
def mock_product_price_bjs():
    with patch('src.modules.price_checker.product_price_bjs') as mock_bjs:
        yield mock_bjs

@pytest.fixture
def mock_product_price_google():
    with patch('src.modules.price_checker.product_price_google') as mock_google:
        yield mock_google

@pytest.fixture
def mock_product_price_amazon():
    with patch('src.modules.price_checker.product_price_amazon') as mock_amazon:
        yield mock_amazon

#Tests for check_price_drop function

def test_check_price_drop_bjs(mock_product_price_bjs):
    mock_product_price_bjs.return_value = "$18.00"
    result = check_price_drop("http://example.com/product", "$20.00", 'bjs')
    assert result == "true"

def test_check_price_drop_google(mock_product_price_google):
    mock_product_price_google.return_value = "$25.00"
    result = check_price_drop("http://example.com/product", "$30.00", 'google')
    assert result == "true"

def test_check_price_drop_amazon(mock_product_price_amazon):
    mock_product_price_amazon.return_value = "$45.00"
    result = check_price_drop("http://example.com/product", "$50.00", 'amazon')
    assert result == "true"