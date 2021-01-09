# Amex Selenium API
Selenium based web page scraper that provides API for getting american express
transactions from your account.

# Pre-Requisites
- Install requirements via `pip install -r requirements.txt`
- Download geckodriver from (here)[https://github.com/mozilla/geckodriver/releases]
  and add it to your path.

# Usage Example
Right now this only supports logging in and retrieving the most recent transactions.

    import amex_selenium
    amex_api = amex_selenium.AmexAPI()
    amex_api.login('YOUR_USERNAME', 'YOUR_PASSWORD')
    transactions = amex_api.get_recent_transactions()

### `AmexAPI.login(username, password)`
Logs into your Amex account. This is the first function that should be called

### `AmexAPI.get_recent_transactions()`
Returns a list of AmexTransaction instances representing your transactions

### AmexTransaction class
This object the following 3 fields
- date - A datetime object representing the date of the transaction (not the time)
- merchant - String - the entity you paid
- amount - float - the amount paid to the merchant
