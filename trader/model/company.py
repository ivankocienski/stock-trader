
class Stock:
    def __init__(self, symbol, share_count, value):
        self.symbol      = symbol
        self.share_count = share_count
        self.value       = value
        

class Company:
    def __init__(self, name, symbol, share_count, value):
        self.stock  = Stock(symbol, share_count, value)
        self.name   = name

class CompanyDB:
    def __init__(self):
        self.db = dict()

    def register(self, symbol, name, volume, price):
        print("Registered company '%s'" % name)
        self.db[symbol] = Company(name, symbol, volume, price)

    def symbols(self):
        return list(self.db.keys())

    def lookup(self, symbol):
        return self.db[symbol]

    def count(self):
        return len(self.db)

    class CompanyIterator:
        def __init__(self, company_db):
            self.company_db = company_db
            self.keys       = company_db.symbols()
            self.pos        = 0

        def __next__(self):
            if self.pos >= len(self.keys):
                raise StopIteration()
            self.pos += 1
            return self.company_db.db[self.keys[self.pos-1]]

    def __iter__(self):
        return self.CompanyIterator(self)
