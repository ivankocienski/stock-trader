
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
                symbol="string")

        # player table
        if db.table_exists('player'):
            print('player exists')
        else:
            print('creating player table')
            db.create_table(
                "player",
                id="integer primary key",
                funds="integer")
            
