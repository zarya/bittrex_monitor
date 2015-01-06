import time
import sys
from blessed import Terminal
from bittrex.bittrex import Bittrex
import ConfigParser
from time import strftime

config = ConfigParser.ConfigParser()
config.read('bot.cfg')

exchange = Bittrex(config.get('Bittrex', 'key'),config.get('Bittrex', 'secret'))

term = Terminal()
print(term.clear())

order_type = {
    'LIMIT_BUY': "LB",
    'LIMIT_SELL': "LS",
    'BUY' : "B",
    'SELL' : "S",
}

def get_balance(coin):
    balance = exchange.get_balance(coin)
    if balance['result'] != None:
        return float(balance['result']['Available'])
    else:
        return 0.00

while True:
    print(term.clear())
    print(term.move(0,1) + term.bold("Bittrex"))
    balances = exchange.get_balances()['result']
    print(term.move(1, 1) + "Wallets")
    line = 2 
    for balance in balances:
        print(term.move(line, 4) + balance['Currency'])
        print(term.move(line, 10) + ": %0.8f" % (balance['Available']))
        line = line + 1

    line = line + 2
    print(term.move(line,1) + "Orders:            Last       Bid        Ask")
    line = line + 1 
    for market in exchange.get_markets()['result']:
        if market['IsActive']:
            name = market['MarketName']
            orders = exchange.get_open_orders(name)['result']
            if len(orders) != 0:
                ticker = exchange.get_ticker(name)['result']
                print(term.move(line, 4) + name)
                print(term.move(line, 15) + ": %s (%0.8f %0.8f %0.8f)" % 
                    (len(orders),ticker['Last'],ticker['Bid'],ticker['Ask']))
                line = line + 1
                for order in orders:
                    print(term.move(line, 8) + "%s %0.2f %0.8f" % 
                        (order_type[order['OrderType']],
                         order['QuantityRemaining'],
                         order['Limit']))
                    line = line + 1
    line = line + 1
    print(term.move(line,1) + "Updated: " + strftime("%Y-%m-%d %H:%M:%S"))
    time.sleep(60)
