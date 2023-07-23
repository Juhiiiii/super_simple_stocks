"""Constants file is a collection of all the constants being used in the assignment.
"""

import enum

@enum.unique
class BuySell(enum.Enum):
    """
        Purpose: Require it to record trade to know whether it was bought or sold.
        Decorator: Uses in built class enum to have unqiue values for required constants
    """
    BUY = 1
    SELL = 2

@enum.unique
class StockType(enum.Enum):
    """
        Purpose: To know what is the type of the stock.
                 Uses formulas required to calculate the necessary based on the type of stock
                 (As required in the assignment)
        Decorator: Uses in built class enum to have unqiue values for required constants
    """
    COMMON = 1
    PREFERRED = 2