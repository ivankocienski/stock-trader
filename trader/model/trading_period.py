
import trader.db as db

class TradingPeriod:
    def __init__(self, row, company_id):
        self.db_id      = int(row[0])
        self.company_id = company_id
        self.start_time = float(row[2])
        self.duration   = float(row[1])
        self.val_open   = float(row[3])
        self.val_close  = float(row[4])
        self.val_high   = float(row[5])
        self.val_low    = float(row[6])

    @staticmethod
    def find_for_company(company_id):
        sql  = 'select'
        sql += '  id, duration, start_time, val_open, val_close, val_high, val_low'
        sql += '  from trading_period'
        sql += '  where company_id=?'
        sql += '  order by start_time DESC'
        args = (company_id,)

        periods = []
        for row in db.execute(sql, args):
            periods.append(TradingPeriod(row, company_id))

        return periods
