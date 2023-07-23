import copy
import enum
import operator
from datetime import datetime, timedelta
from functools import reduce
from constants import BuySell, StockType

class Stock_Details:
    """
    The attributes of Stock_Details are as follows:

    symbol - the symbol/name of the stock
    stock_type - the type of the stock
    timestamp - to record the time the trade took place
    quantity - number of shares
    price_per_share - cost of each share
    buy_sell - whether the share was bought or sold

    """

    def __init__(self, symbol, stock_type: StockType, 
                 timestamp: datetime, 
                 quantity,price_per_share,
                 buy_sell: BuySell):
        
        """
        Initializing the required attributes with error handling.
        """

        self.symbol = symbol
        if type(stock_type) is StockType:
            self.stock_type = stock_type
        else:
            raise ValueError('Stock Type is invalid')
        self.timestamp = timestamp
        if quantity > 0:
            self.quantity = quantity
        else:
            raise ValueError('The quantity is invalid')
        if price_per_share >= 0.0:
            self.price_per_share = price_per_share
        else:
            raise ValueError('Stock price entered is invalid')
        self.buy_sell = buy_sell

    @property
    def total_price(self):
        """
        Purpose: Calculates the total price
        Formula: quantity * cost of each share
        Returns: total price of the share
        """
        return self.quantity * self.price_per_share

class Stock:
    """
    Purpose: Contains attributes and functions for all required calculations for the following:
                a. For a given stock, 
                    i. Given any price as input, calculate the dividend yield
                    ii. Given any price as input, calculate the P/E Ratio
                    iii. Record a trade, with timestamp, quantity of shares, buy or sell indicator and 
                    traded price
                    iv. Calculate Volume Weighted Stock Price based on trades in past 15 minutes
    """
    price_time_interval = timedelta(minutes=15)

    def __init__(self,
                 symbol: str,
                 stock_type: StockType,
                 par_value: float,
                 last_dividend: float,
                 fixed_dividend: float):
        """
        The attributes of Stock are as follows:

            symbol - the symbol/name of the stock
            stock_type - the type of the stock
            last_dividend - the value of the last divident
            par_value - the par value of each share
            fixed_dividend - the value of the fixed dividend (Only present when stock type is preferred)
            self trades - List to record all the trades.
        """
        self.symbol = symbol
        self.stock_type = stock_type
        self.par_value = par_value
        self._last_dividend = last_dividend
        if self.stock_type is StockType.COMMON and fixed_dividend is not None:
            raise ValueError('Incorrect data')
        else:
            self._fixed_dividend = fixed_dividend

        self.trades = []

    @property
    def dividend(self):
        """
        calculates the dividend
        """
        if self.stock_type is StockType.COMMON:
            return float(self._last_dividend)
        else:
            return self._fixed_dividend * self.par_value

    @property
    def dividend_yield(self):
        return self.dividend / self.ticker_price

    def record_trade(self, trade: Stock_Details):
        """
        Records a trade
        """
        if type(trade) is not Stock_Details:
            raise TypeError('Incorrect type')
        elif self.symbol is not trade.symbol or self.stock_type is not trade.stock_type:
            raise ValueError('incorrect stock')
        else:
            self.trades.append(trade)

    @property
    def last_stock_price(self):
        """
        Returns the last recorded price of a stock
        """
        if len(self.trades) > 0:
            return float(self.trades[-1].price_per_share)
        else:
            raise AttributeError('Last recorded price is unavailable')

    @property
    def pe_ratio(self):
        """
        Calculates and Returns the PE Ratio
        """
        if self.dividend != 0:
            return self.last_stock_price / self.dividend
        else:
            return None

    def stock_price(self, current_time: datetime=datetime.now()):
        """
        Returns the Stock Price based on trades in past 15 minutes
        """
        trade_time =  [trade for trade in self.trades
                              if trade.timestamp >= current_time - self.price_time_interval]

        if len(trade_time) > 0:
            summed_price = sum([trade.total_price for trade in trade_time])
            quantities = sum([trade.quantity for trade in trade_time])
            return summed_price / float(quantities)
        else:
            return None
        
    def all_share_index(self, current_time: datetime=datetime.now()):
        """
        Returns all share index
        """
        n = len(self.trades)
        price_all_stocks = [stock.stock_price(current_time) for stock in self.trades]

        if None in price_all_stocks:
            return None
        else:
            product = reduce(operator.mul, price_all_stocks, 1)
            return product**(1/n)
