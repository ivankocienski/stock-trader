
import trader.db as db

class PlayerStock():
    def __init__(self, player, company):
        self.company  = company
        self.player   = player
        self.quantity = 0
        self.db_id    = None
        
        sql  = 'select player_stock.id, quantity'
        sql += '  from player_stock, company'
        sql += '  where company.id=company_id and company.symbol=(?)'
        args = (company.symbol,)
        row = db.execute_one(sql, args)
        if row: 
            print("player_stock: company already exists")
            self.quantity = row[1]
            self.db_id = row[0]

    def _save_to_db(self):
        if self.db_id:
            sql  = 'update player_stock'
            sql += '  set quantity=(?)'
            sql += '  where id=(?)'
            args = (self.quantity, self.db_id)
            db.execute_one(sql, args)

        else:
            sql  = 'insert into player_stock'
            sql += '  (company_id, player_id, quantity)'
            sql += '  values (?, ?, ?)'
            args = (self.company.db_id, self.player.db_id, self.quantity)
            self.db_id = db.execute_id(sql, args)
            print("player_stock: save_to_db: INSERT id=%s"%self.db_id)

        db.commit()

    def buy(self, buy_quantity): 
        print("buy stock q=%d  c='%s'" % (buy_quantity, self.company.name))
        
        cost = buy_quantity * self.company.share_value
        print("cost=%d"%cost)
        if cost > self.player.funds:
            print("insufficient funds")
            return False 

        self.player.funds -= cost
        self.quantity += buy_quantity

        self._save_to_db() 

        return True

    def sell(self, quantity):
        if quantity > self.quantity:
            return False

        profit = quantity * company.stock_value
        self.player_funds += profit

        return True

    def value(self):
        return self.quantity * self.company.share_value

    def is_zero(self):
        return self.quantity == 0

class Player:
    def __init__(self, company_db):
        self.owned_stock = dict()
        self.company_db = company_db
        self.db_id = 0
        self.funds = 0
        self.owned_stock_symbols = []
        self.load()
        
    def save(self):
        sql  = 'update player set funds=? where id=?'
        args = (self.funds, self.db_id)
        db.execute_one(sql, args)
        db.commit()

    #def owned_stock_symbols(self):
    #    symbols = list(self.owned_stock.keys())
    #    symbols.sort()
    #    return symbols

    def retrieve(self, symbol):
        stock = None 
        try:
            stock = self.owned_stock[symbol]

        except KeyError:
            company = self.company_db.lookup(symbol)
            stock = PlayerStock(self, company)
            if stock:
                self.owned_stock[symbol] = stock 
            else:
                return None

        return stock

    def load(self):
        sql = 'select id, funds from player'
        row = db.execute_one(sql)
        
        self.db_id = int(row[0])
        self.funds = int(row[1])

        # oh to have a nice s-exp DSL about now -.-
        sql  = 'select company.symbol'
        sql += '  from player_stock, company'
        sql += '  where company_id = company.id order by symbol'
        for row in db.execute(sql):
            self.owned_stock_symbols.append(row[0])

    def buy_stock(self, company, quantity):
        stock = None

        try:
            stock = self.owned_stock[company.symbol]

        except KeyError:
            stock = PlayerStock(self, company)
            self.owned_stock[company.symbol] = stock 

        okay = stock.buy(quantity)
        if okay:
            self.save()

        return okay


    def sell_stock(self, company, quantity):
        stock = None
        try:
            stock = self.owned_stock[company.symbol]

        except KeyError:
            return False

        okay = stock.sell(quantity)
        if okay:
            # TODO: purge records where quantity is zero
            self.save()

        return okay

    def total_value(self):
        value = 0
        print("total_value")
        print(self.owned_stock)
        for symbol, stock in self.owned_stock.items():
            value += stock.value()

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
