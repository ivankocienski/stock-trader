
import csv
import os
import random

import trader.db as db

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

    def run(self):

        self._generate_companies()
        self._generate_player()


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


