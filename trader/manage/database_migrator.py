
import trader.db as db

class DatabaseMigrator:

    def run(self):
        
        # company table
        if db.table_exists('company'):
            print("company exists")
        else:
            print("company does not exist")
            db.create_table(
                "company",
                id="integer primary key",
                name="string",
                symbol="string",
                share_count="integer",
                share_value="real")

        # trading period table
        if db.table_exists('trading_period'):
            print("trading_period exists")
        else:
            db.create_table(
                'trading_period',
                id='integer primary key',
                company_id='integer not null',
                duration='integer not null',
                start_time='real',
                val_open='real',
                val_close='real',
                val_high='real',
                val_low='real')

        # player table
        if db.table_exists('player'):
            print('player exists')
        else:
            print('creating player table')
            db.create_table(
                "player",
                id="integer primary key",
                funds="integer")
            
        # player stock table
        if db.table_exists('player_stock'):
            print('player_stock exists')
        else:
            print('create player_stock table')
            db.create_table(
                'player_stock',
                id='integer primary key',
                player_id='integer not null',
                company_id='integer not null',
                quantity='integer not null')

        
