from configparser import ConfigParser


class ConfLoader:
    def __init__( self, conf_path ):
        parser = ConfigParser()
        parser.read( conf_path )
        self.site_url = parser.get( 'targeting', 'site_url' )
        self.brand_id = parser.get( 'targeting', 'brand_id' )
        self.username = parser.get( 'user', 'username' )
        self.password = parser.get( 'user', 'password' )


def Main():
    conf = ConfLoader('Conf/configuration.ini')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
