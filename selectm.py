from configparser import ConfigParser
import requests


class ConfLoader:
    def __init__( self, conf_path ):
        parser = ConfigParser()
        parser.read( conf_path )
        self.site_url = parser.get( 'targeting', 'site_url' )
        self.brand_id = parser.get( 'targeting', 'brand_id' )
        self.username = parser.get( 'user', 'username' )
        self.password = parser.get( 'user', 'password' )


class Session:
    def __init__( self, conf ):
        self.client = requests.Session()
        self.conf = conf

    def login(self):
        pass

def Main():
    conf = ConfLoader('Conf/configuration.ini')
    session = Session( conf )
    session.login()


if __name__ == '__main__':
    Main()
