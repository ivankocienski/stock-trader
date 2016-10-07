
import trader.db as db

#class Stock:
#    def __init__(self, symbol, share_count, value):
#        self.symbol      = symbol
#        self.share_count = share_count
#        self.value       = value
        

class Company:
    #def __init__(self, name, symbol, share_count, value):
    #    self.stock  = Stock(symbol, share_count, value)
    #    self.name   = name

    def __init__(self, row):
        #print(row)
        self.db_id = row[0]
        self.name = row[1]
        self.symbol = row[2]

        value = row[3]
        if value is None:
            value = 0
        else:
            value = int(value)

        self.share_count = value

        value = row[4]
        if value is None:
            value = 0
        else:
            value = int(value)

        self.share_value = value

        #print(self)

    def __str__(self):
        return "<company name='%s', symbol='%s'>"%(self.name, self.symbol)

class CompanyDB:
    #def __init__(self):
    #    pass
    #    self.db = dict()

    #def register(self, symbol, name, volume, price):
    #    print("Registered company '%s'" % name)
    #    self.db[symbol] = Company(name, symbol, volume, price)

    def symbols(self):
        found = []
        for row in db.execute('select symbol from company order by symbol'):
            found.append(row[0])
        return found

    def lookup(self, symbol):
        fields = 'id, name, symbol, share_count, share_value'
        sql = 'SELECT %s from company WHERE symbol=(?)' % fields
        args = (symbol,)
        result = db.execute_one(sql, args)
        if result is None:
            return None

        return Company(result)

    def count(self):
        return db.count_table('company')

    class CompanyIterator:
        def __init__(self, company_db):
            self.company_db = company_db
            self.keys       = company_db.symbols()
            self.pos        = 0

        def __next__(self):
            if self.pos >= len(self.keys):
                raise StopIteration()
            self.pos += 1
            return self.company_db.lookup(self.keys[self.pos-1])

    def __iter__(self):
        return self.CompanyIterator(self)
