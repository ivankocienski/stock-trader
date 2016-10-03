
class Player:
    def __init__(self, company_db):
        self.funds = 1000
        self.owned_stock = dict()
        self.company_db = company_db

    def buy_stock(self, company, quantity):
        print("buy stock q=%d  c='%s'" % (quantity, company.name))
        
        cost = quantity * company.stock.value
        if cost > self.funds:
            return False

        print("cost=%d"%cost)

        self.funds -= cost
        if company.stock.symbol in self.owned_stock:
            self.owned_stock[company.stock.symbol] += quantity
        else:
            self.owned_stock[company.stock.symbol] = quantity

        return True
        
    def total_value(self):
        value = 0
        for symbol, quantity in self.owned_stock.items():
            value += quantity * self.company_db.lookup(symbol).stock.value;

        return value
