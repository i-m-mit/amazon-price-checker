# imports
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import re
import smtplib
import json
import time

# load env variables
load_dotenv()

# Constants

# env variable keys
ENV_USER_MAIL_ADDRESS_KEY = "USER_MAIL_ADDRESS"
ENV_RECEIVER_MAIL_ADDRESS_KEY = "RECEIVER_MAIL_ADDRESS"
ENV_PASSWORD_KEY = "PASSWORD"

# dictionary keys
PRODUCT_KEY = "products"
URL_KEY = "URL"
PRICE_KEY = "price"
TITLE_KEY = "product_title"

# header for request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}


def load_files() -> dict:
    """
    Loads products.json file and returns the content in dictionary format.

    @return: products dictionary

    Note: products.json file should be in same directory.
    """
    products = None
    with open("products.json", "r", encoding="utf-8-sig") as json_file:
        try:
            file_content = json_file.read()
            products = json.loads(file_content)
            print("FILE LOADED!!")
        except Exception as e:
            print(e)
        finally:
            json_file.close()
    return products


def check_price(URL, expected_price) -> None:
    """
    Retrieves the Amazon.in page of product and checks the price.

    Adds product URL and Product title in list_products_in_budget if the price has dropped
    """
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        price_txt = soup.find(id="priceblock_ourprice").get_text()
    except:
        try:
            price_txt = soup.find(id="priceblock_dealprice").get_text()
        except:
            return

    price = float(re.sub("\D", "", price_txt)[:-2])
    product_title = soup.find(id="productTitle").get_text().strip()

    if price <= expected_price:
        list_products_in_budget.append({URL_KEY: URL, TITLE_KEY: product_title})


def send_mail() -> None:
    """
    Send the mail to receiver alerting him/her about price drop
    """
    # set up smtp server
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # get evn variables for mail
    user_mail = os.getenv(ENV_USER_MAIL_ADDRESS_KEY)
    receiever_mail = os.getenv(ENV_RECEIVER_MAIL_ADDRESS_KEY)
    password = os.getenv(ENV_PASSWORD_KEY)

    server.login(user_mail, password)

    # format e-mail
    subject = "Price Fall Down!!"
    body = "Price fell down for following products:\n\n"
    for product in list_products_in_budget:
        body = body + f"{product[TITLE_KEY]}: {product[URL_KEY]}\n\n"
    msg = f"Subject: {subject}\n\n{body}"

    # send mail
    server.sendmail(user_mail, receiever_mail, msg)

    print("MAIL SENT!!")
    server.quit()


products = load_files()
if products is not None:
    products = products[PRODUCT_KEY]
    while True:

        # empty the list of products that are in budget
        list_products_in_budget = []

        # loop to check each product in products dictionary
        for product in products:
            check_price(product[URL_KEY], product[PRICE_KEY])

        # if there are some products for which the price has dropped,
        # then notify user with mail
        if len(list_products_in_budget) > 0:
            send_mail()

        # check every 6 hours
        time.sleep(60 * 60 * 6)