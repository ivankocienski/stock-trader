
from sys import argv
from pathlib import Path
import os

from trader.manage.company_seeder import CompanySeeder
from trader.manage.database_migrator import DatabaseMigrator

import trader.db as db

class DoDBSetup:
    name = 'db-setup'
    def invoke(self, args):
        print("Setting up database")

        path = os.getcwd()
        path += '/state/database.sqlite3'

        p = Path(path)
        if p.exists():
            print("database exists")
            print("Please delete '%s' and run again"%path)
            return

        db.init(path)

        migrator = DatabaseMigrator()
        migrator.run()

        seeder = CompanySeeder()
        seeder.run()

        seeder.fake_player_stock()

class DoHelp:
    name = 'help'
    def invoke(self, args):
        print("help")

class DoDBStats:
    name = 'db-stats'

    def _count_table(self, name):
        sql = 'select count(*) from %s'%name
        count = db.execute_one(sql)[0]
        print("%s count %s"%(name, count))

    def invoke(self, args):
        print("DB Stats")

        path = os.getcwd()
        path += '/state/database.sqlite3'
        db.init(path)

        self._count_table('company')
        self._count_table('player')
        self._count_table('player_stock')
        self._count_table('trading_period')


class Manager:

    def _register_command(self, obj):
        self.commands[obj.name] = obj()

    def _invoke_command(self, name, args):
        self.commands[name].invoke(args)

    def _bad_arg(self, message):
        print("%s, try"%message)
        for cmd in self.commands:
            print(cmd)

    def __init__(self): 
        self.commands = dict()

        self._register_command(DoHelp)
        self._register_command(DoDBSetup)
        self._register_command(DoDBStats)

    def run(self):
        args = argv[1:]

        if len(args) == 0:
            self._bad_arg('No command given')
            return

        try: 
            self._invoke_command(args[0], args[1:])
        except KeyError:
            self._bad_arg('Unrecognised command given')




if __name__ == '__main__': Manager().run()
