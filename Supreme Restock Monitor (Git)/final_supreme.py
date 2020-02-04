
"""

This script monitors products on Supreme NewYork's online webstore using
Discord notifications.

"""

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordEmbed
from datetime import datetime
import time
import sys

# ---This web url cannot be spread out between seperate lines---#
webhook_url=('')

class Product:

    """
    This is a class for making product objects for each of supreme's online
    order.

    Attributes:
        product_link (int): A list of product web links.
        image_link (list): A list of product images links.
        stock (boolean): True/False values representing whether or not an item
                         is in stock or not.
    """

    def __init__(self,product_link,image_link,stock):

        """
        The constructor for the Product class.

        Parameters:
            product_link (int): A list of product web links.
            image_link (list): A list of product images links.
            stock (boolean): True/False values representing whether or not an
                             item is in stock or not.
        """

        self.product_link = product_link
        self.image_link = image_link
        self.stock = stock

def get_page():

    """

    Uses BeautifulSoup to make requests to get the HTML info for the website.

    Returns:
        (page): returns the HTML outline of Supreme's website.

    """

    link = "http://www.supremenewyork.com/shop/all"
    get_page = requests.get(link,timeout=5, verify=True)
    page = BeautifulSoup(get_page.text, 'html.parser')

    return page

def build_product_list(page):

    """

    Uses the html page layout, parses it, and uses the information to create
    a product object for each product on Supreme's website.

    Args: page (html): the HTML page layout for Supreme's website.

    Returns:
        (product_list): returns a list of product objects for each Supreme
                        product.

    """


    product_list = []
    raw_product_link = page.findAll("div", {"class": "inner-article"})

    for links in raw_product_link:

        product_link = "https://www.supremenewyork.com" + links.a["href"]

        image_link = "https:" + links.a.img["src"]

        if(links.text == "sold out"):
            stock = False
        else:
            stock = True
        product_list.append(Product(product_link,image_link,stock))

    return product_list


def get_descriptions(products):

    """

    Gets the corresponding product description for each product link.

    Args: products (list): a list of product objects.

    Returns:
        (all_descriptions): returns a dictionary with a product link as a key,
                          and the product's corresponding description as a val.

    """


    all_descriptions = {}
    for product in products:
        get_page = requests.get(product.product_link,timeout=5, verify=True)
        new_page = BeautifulSoup(get_page.text, 'html.parser')
        descriptions = new_page.find_all('title')

        for description in descriptions:
            description = (description.get_text())
        all_descriptions[product.product_link] = description

    return all_descriptions


def monitor(old_list,new_list,webhook_url,all_descriptions):

    """

    detects differences inbetween product object lists, and sends a Discord
    notification based upon the changes.

    Args: old_list (list): an old list of Product_objects.
          new_list (list): a new list of Product_objects.
          webhook_url (str): the link for the Discord Channel.
          all_descriptions (dictionary): the dictionary with each product desc.

    """

    values = []

    for old,new in zip (old_list, new_list):

        if old.stock != new.stock and old.product_link != new.product_link:

            # print('Stock/Product change')
            new.description = all_descriptions[new.product_link]
            values.append(new.product_link)
            values.append(new.description)
            values.append(new.image_link)
            values.append(new.stock)

            send_alert(webhook_url,values,'NEW PRODUCTS!')

        elif old.stock != new.stock:

            # print('Stock/Product change')
            new.description = all_descriptions[new.product_link]
            values.append(new.product_link)
            values.append(new.description)
            values.append(new.image_link)
            values.append(new.stock)

            send_alert(webhook_url,values,'RESTOCK!')

def send_alert(webhook_url,values,alert_type):

    """

    Sends alerts through the discord channel when a product restcks, or
    Supreme's updates their website with new products.

    Args: webhook_url (str): the link for the Discord Channel.
          values (list): a list of item attributes, in addition to
                         descriptions.
          alert_type (str): the str for the type restock/product change
                            that occured.

    """

    webhook = DiscordWebhook(webhook_url)

    embed = DiscordEmbed(title = alert_type + '\n' + values[1] ,
            description = values[0], color=202424)

    embed.set_author(name='Jon-Bon', icon_url= 'https://fontmeme.net/permalink/190420/a36efebd709428bdf6c6fb754a780184.png')

    embed.set_image(url= values[2])

    embed.set_thumbnail(url='https://fontmeme.net/permalink/190420/a36efebd709428bdf6c6fb754a780184.png')

    embed.set_footer(text='Products')

    embed.set_timestamp()

    webhook.add_embed(embed)

    webhook.execute()

def main(webhook_url):

    """

    Calls/runs all the scripts' functions.

    Args: webhook_url (str): the Discord apps webhook address.

    """

    page = get_page()
    old_list = build_product_list(page)
    all_descriptions = get_descriptions(old_list)

    while(True):

        time.sleep(8)
        page = get_page()
        new_list = build_product_list(page)
        monitor(old_list,new_list,webhook_url,all_descriptions)
        print('searching for restocks.. please wait.')
        old_list = new_list

if __name__ == '__main__':

    main(webhook_url)
