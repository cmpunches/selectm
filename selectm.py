from configparser import ConfigParser
import requests
import sys
from lxml import html
import json



class Product:
    def __init__( self, brand_id, brand_family_id, product_name, available ):
        self.brand_id = brand_id
        self.brand_family_id = brand_family_id
        self.product_name = product_name
        self.available = available

    def __str__(self):
        return "[ Available: {3} ] {2} (Brand: {0}/ Family: {1})".format( self.brand_id, self.brand_family_id, self.product_name, self.available )


class ConfLoader:
    def __init__( self, conf_path ):
        parser = ConfigParser()
        parser.read( conf_path )
        self.site_url = parser.get( 'targeting', 'site_url' )
        self.brand_id = parser.get( 'targeting', 'brand_id' )
        self.barrels  = parser.get( 'targeting', 'barrels')
        self.username = parser.get( 'user', 'username' )
        self.password = parser.get( 'user', 'password' )

class InteractionClient:
    def __init__( self, conf ):
        self.client = requests.Session()
        self.client.headers.update(
            {
                'User-Agent': "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",

            }
        )
        self.conf = conf
        self.inventory = list()

    def login(self):
        headers = {
            'Host': self.conf.site_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': "https://{0}".format( self.conf.site_url ),
            'Connection': 'keep-alive',
            'Referer': "https://{0}/login".format( self.conf.site_url )
        }

        data = {
            '_method': 'POST',
            'data[AppUser][email]': self.conf.username,
            'data[AppUser][password]': self.conf.password,
            'data[User][return_to]': '',
            'data[AppUser][remember_me]': '0'
        }

        login_url = "https://{0}/app_users/login".format( self.conf.site_url )
        response = self.client.post( login_url, headers=headers, data=data )
        if response.status_code in [ 200, 301, 302 ]:
            print("Login successful.")
        else:
            print( "Login failed.", file=sys.stderr )
            exit(1)

    def update_inventory(self):
        inventory_pull = list()

        inventory_url = "https://{0}/orders/create-order".format( self.conf.site_url )
        response = self.client.get( inventory_url )
        if not response.status_code in [ 200, 301, 302 ]:
            print( "Failed to fetch inventory.", file=sys.stderr )
            exit(1)

        deserialized_response = html.fromstring( response.text )
        product_listings_raw = deserialized_response.xpath('//*/div[@class="brands"]/div[@class="row"]/div')
        for listing in product_listings_raw:
            brand_family_id = listing.attrib['class'].split()[-1].split('-')[-1]
            product_name = listing.xpath('*/h2[@class="brand-name"]/text()')[0]
            brand_id = listing.xpath('*/div[@class="add-to-order"]/input[@id="brand_id"]')[-1].value

            availability_raw = None
            try:
                availability_raw = listing.xpath('*/div[@class="add-to-order"]/button[@disabled="disabled"]/text()')[-1]
            except:
                availability_raw = None

            if availability_raw is None:
                availability = True
            else:
                availability = False

            this_listing = Product(
                brand_id=brand_id,
                brand_family_id=brand_family_id,
                product_name=product_name,
                available=availability
            )

            inventory_pull.append( this_listing )
        self.inventory = inventory_pull

    def item_is_available(self, brand_id ):
        for item in self.inventory:
            if item.brand_id == brand_id:
                print("Found item: {0}".format(item))
                if item.available:
                    return True
        print("Not available.")
        return False

    def get_item_from_inventory(self, brand_id=None, product_name=None ):
        retVal = None

        if (brand_id is None and product_name is None) or (brand_id is not None and product_name is not None):
            print( "Must provide ONE OF either a brand_id or product_name to pull an item from inventory.", file=sys.stderr )
            exit(1)

        if product_name is not None:
            for item in self.inventory:
                if item.product_name == product_name:
                    retVal = item

        if brand_id is not None:
            for item in self.inventory:
                if item.brand_id == brand_id:
                    retVal = item

        return retVal

    def add_to_cart( self, item ):
        headers = {
            'Host': self.conf.site_url,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': "https://{0}/orders/create-order".format( self.conf.site_url )
        }
        data = {
            'brandId': item.brand_id,
            'numBarrels': self.conf.barrels,
            'brandFamilyId': item.brand_family_id
        }

        cart_url = "https://{0}/orders/selected-brands".format( self.conf.site_url )
        response = self.client.post( cart_url, headers=headers, data=data )
        if response.status_code in [ 200, 301, 302, 201 ]:
            try:
                response_obj = json.loads( response.text )
                if len(response_obj['successMessages']) > 0:
                    print("Successfully added to cart.")
                else:
                    print("Got a successful HTTP response but body did not indicate success.", file=sys.stderr)
                    exit(1)
            except:
                print("Got a non-json response and expected a json response.", file=sys.stderr)
                exit(1)
        else:
            print( "Failed to add item '{0}' to cart.".format( item.product_name ), file=sys.stderr )
            exit(1)

def Main():
    conf = ConfLoader( 'Conf/configuration.ini' )
    session = InteractionClient( conf )
    session.login()
    session.update_inventory()

    if session.item_is_available( brand_id=conf.brand_id ):
        item = session.get_item_from_inventory( brand_id=conf.brand_id )
        print( "The item '{0}' is available for purchase.".format( item.product_name ) )
        session.add_to_cart( item )
    else:
        print( "The configured item is not available.", file=sys.stderr )


if __name__ == '__main__':
    Main()
