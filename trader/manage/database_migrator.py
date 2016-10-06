
import trader.db as db

class DatabaseMigrator:

    def run(self):
        if db.table_exists('company'):
            print("company exists")
        else:
            print("company does not exist")
            db.create_table(
                "company",
                id="integer primary key",
                name="string",
                symbol="string")

        count = db.count_table('company')
        print("company has %d rows"%count)


