# Amazon Price Checker

We often like some product on Amazon.com, but led down by our budget.

Worry no more!! This project may come in handy for such situations.

This is a simple scrapper project using `BeautifulSoup` and `requests` libraries of python, which tracks down the price and notifies you whenever a item you mentioned in `products.json` file comes down to your price.

**Note:** Example `product.json` file is present in repository.

## Prerequisite

* Python - [Download Pyhton using this link](https://www.python.org/downloads/)
* BeautifulSoup - `pip install bs4`
* Requests - `pip install requests`
* DotEnv - `pip install python-dotenv`

**Note:** Please install required packages using the following command

```
pip install -r requirements.txt
```

## Format of .env file

Generate a new file named `.env` and paste following text into it.

Replace values in quotes with user's values

```
USER_MAIL_ADDRESS="user_mail_address"
PASSWORD="gmail_app_password"
RECEIVER_MAIL_ADDRESS="receiver_mail_address"
```

**Note:** Please refer [How to generate Google App Password](https://support.google.com/mail/answer/185833?hl=en-GB)

For more information about `.env` file visit [documentation](https://pypi.org/project/python-dotenv/)


## Final Step

After adding your favourite products' **URL** and **Expected Price** run your `scraper.py` file using following command

```
> python scraper.py
```

Script is designed to check for the price drop every 6 hours, but you can customize it to check on your own time.