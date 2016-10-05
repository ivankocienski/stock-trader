
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

    def sell_stock(self, company, quantity):
        if quantity > self.owned_stock[company.stock.symbol]:
            return False

        profit = quantity * company.stock.value
        self.funds += profit

        self.owned_stock[company.stock.symbol] -= quantity
        if self.owned_stock[company.stock.symbol] == 0:
            del self.owned_stock[company.stock.symbol]

        return True

    def owned_stock_symbols(self):
        return list(self.owned_stock.keys())
        
    def total_value(self):
        value = 0
        for symbol, quantity in self.owned_stock.items():
            value += quantity * self.company_db.lookup(symbol).stock.value;

        return value

    class PlayerIterator:
        def __init__(self, player_obj):
            self.symbol_list = list(player_obj.owned_stock.keys())
            self.symbol_pos  = 0
            self.player = player_obj

        def __next__(self):
            if self.symbol_pos >= len(self.symbol_list):
                raise StopIteration()

            self.symbol_pos += 1
            sym = self.symbol_list[self.symbol_pos-1]
            return (sym, self.player.owned_stock[sym])

    def __iter__(self):
        return self.PlayerIterator(self)
