
import trader.db as db

class PlayerStock():
    def __init__(self, player, company):
        self.company  = company
        self.player   = player
        self.quantity = 0

    def buy(self, buy_quantity): 
        print("buy stock q=%d  c='%s'" % (buy_quantity, self.company.name))
        
        cost = buy_quantity * self.company.share_value
        print("cost=%d"%cost)
        if cost > self.player.funds:
            print("insufficient funds")
            return False 

        self.player.funds -= cost
        self.quantity += buy_quantity

        return True

    def sell(self, quantity):
        if quantity > self.quantity:
            return False

        profit = quantity * company.stock_value
        self.player_funds += profit

        return True

    def is_zero(self):
        return self.quantity == 0

class Player:
    def __init__(self, company_db):
        self.owned_stock = dict()
        self.company_db = company_db
        self.funds = 0
        self.load()
        
    def save(self):
        sql  = 'update player set funds=(?)'
        args = (self.funds,)
        db.execute_one(sql, args)

    def load(self):
        sql = 'select funds from player'
        row = db.execute_one(sql)
        
        self.funds = int(row[0])
        self.owned_stock_symbols = []

        # oh to have a nice s-exp DSL about now -.-
        sql = 'select company.symbol from player_stock, company where company_id = company.id order by symbol'
        for row in db.execute(sql):
            self.owned_stock_symbols.append(row[0])

#    def _retrieve_stock(self, symbol):
#        try:
#            return self.owned_stock[symbol]
#
#        except KeyError:
#            ps = PlayerStock(symbol)
#            self.owned_stock[symbol] = ps
#            return ps

        

    def buy_stock(self, company, quantity):
        stock = None

        try:
            stock = self.owned_stock[company.symbol]

        except KeyError:
            stock = PlayerStock(self, company)
            self.owned_stock[company.symbol] = stock 

        return stock.buy(quantity)

#
#    def sell_stock(self, company, quantity):
#        return True

    def total_value(self):
        value = 0
        #for symbol, quantity in self.owned_stock.items():
        #    value += quantity * self.company_db.lookup(symbol).stock.value;

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
