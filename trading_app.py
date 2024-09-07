from platform_connector.platform_connector import PlatformConnector

if  __name__ == '__main__':
    symbols = ["AUDCAD", "EURUSD", "USDCHF", "TEST"]
    CONNECT = PlatformConnector(symbol_list=symbols)
