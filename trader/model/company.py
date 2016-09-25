
class Stock:
    def __init__(self, symbol, share_count, value):
        self.symbol      = symbol
        self.share_count = share_count
        self.value       = value
        

class Company:
    def __init__(self, name, symbol, share_count, value):
        self.stock  = Stock(symbol, share_count, value)
        self.name   = name

