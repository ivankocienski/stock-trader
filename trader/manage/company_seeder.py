
import csv
import os
import random
import datetime

import trader.db as db

class TradingPeriodGenerator:


    class Mover:
        def __init__(self, hold_range, value_multiplier):
            self.value_multiplier = value_multiplier
            self.hold_min = hold_range[0]
            self.hold_max = hold_range[1]
            self.hold = 0
            self.inc  = 0

        def move(self):
            if self.hold == 0:
                self.hold = random.randint(
                    self.hold_min,
                    self.hold_max)
            else:
                self.hold -= 1
                return

            base = 1 - random.random() * 2.0 
            self.inc = base * self.value_multiplier


    class StockValue:
        def __init__(self, start_at):

            self.movers = [
                TradingPeriodGenerator.Mover((2,   5),  0.00001),
                TradingPeriodGenerator.Mover((10, 20),  0.0002),
                TradingPeriodGenerator.Mover((30, 50),  0.0001),
                TradingPeriodGenerator.Mover((50, 100), 0.00001),
                TradingPeriodGenerator.Mover((75, 200), 0.0000001)]

            self.real_value  = start_at
            self.value = self.real_value
            self.history = [self.real_value] * 4 

            self.reset_trackers()

        def reset_trackers(self):
            self.value_open  = self.value
            self.value_low   = self.value
            self.value_high  = self.value

        def tick(self):
            delta = 0
            for m in self.movers:
                m.move() 
                delta += m.inc

            self.real_value += delta / len(self.movers)

            self.history.insert(0, self.real_value)
            self.history = self.history[:4]
            self.value = sum(self.history) / 4.0

            if self.value < self.value_low:
                self.value_low = self.value

            if self.value > self.value_high:
                self.value_high = self.value

    def __init__(self, company_id, start_at, period_size, num_periods):
        self.company_id = int(company_id)
        self.start_at = start_at
        self.period_size = period_size
        self.num_periods = num_periods

    def run(self):
        print("Generating trading period data company_id=%s"%self.company_id)

        time = self.start_at - self.num_periods * self.period_size
        stock = TradingPeriodGenerator.StockValue(random.randint(100, 100000))

        for x in range(0, self.num_periods):
            
            stock.reset_trackers()

            for i in range(0, self.period_size):
                stock.tick()

            sql = 'insert into trading_period (company_id, duration, start_time, val_open, val_close, val_high, val_low) values (?, ?, ?, ?, ?, ?, ?)'
            args = (
                self.company_id,
                self.period_size,
                time,
                stock.value_open,
                stock.value,
                stock.value_high,
                stock.value_low)
            
            db.execute_one(sql, args)
            time += self.period_size

        db.commit()


class CompanySeeder:

    def _generate_companies(self):
        db.execute_one('delete from company')

        companies = []
        path = os.getcwd()
        path += '/data/companies-and-stock-symbols.csv'
        with open(path, newline='') as csvfile:

            company_reader = csv.reader(csvfile)

            for row in company_reader:
                companies.append(row)

        print("Loaded %d source companies"%len(companies))

        def random_order(n):
            return random.randint(0, 100000)

        companies.sort(key=random_order)

        count = random.randint(200, 500)
        for company in companies[:count]:
            sql = "insert into company (name, symbol, share_count, share_value) values (?, ?, ?, ?)"
            count = random.randint(20, 2000)
            value = random.randint(100, 5000)
            args = (company[1], company[0], count, value)
            db.execute_one(sql, args)

        db.commit() 
        print("Generated %d companies"%count)

    def _generate_player(self):

        sql = "insert into player (funds) values (?)"
        args = (1000,)
        db.execute_one(sql, args)

        db.commit()
        print("Generated 1 player")

    def _generate_trading_periods(self):
        sql = 'select id from company'

        now = datetime.datetime.now().timestamp()
        period_size = 60 # seconds
        num_periods = 1440 # one day

        print("generating trading periods")

        for com in db.execute(sql):
            tpg = TradingPeriodGenerator(
                com[0], 
                now,
                period_size,
                num_periods)
            tpg.run()

    def run(self):

        self._generate_companies()
        self._generate_player()
        self._generate_trading_periods()


    def fake_player_stock(self):

        company_ids = []
        for com in db.execute('select id from company'):
            company_ids.append(int(com[0]))

        player_id = int(db.execute_one('select id from player')[0])

        print("company_ids count %d"%len(company_ids))
        print("player_id=%d"%player_id)

        for cid in company_ids:
            sql = "insert into player_stock"
            sql += "  (company_id, player_id, quantity)"
            sql += "  values (?, ?, ?)"
            args = (cid, player_id, random.randint(2, 20))
            db.execute_one(sql, args)

        db.commit()


