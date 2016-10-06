
import csv
import os
import random

import trader.db as db

class CompanySeeder:
    def run(self):
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
            sql = "insert into company (name, symbol) values (?, ?)"
            args = (company[0], company[1])
            db.execute_one(sql, args)

        db.commit()

        print("Generated %d companies"%count)

