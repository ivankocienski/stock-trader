
import sqlite3

db = None

def init(path): 
    global db
    print("using database '%s'"%path)
    db = sqlite3.connect(path)

def execute_one(sql, args=()):
    global db
    cur = db.cursor()
    cur.execute(sql, args)
    return cur.fetchone()

def table_exists(name):
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=(?)"
    result = execute_one(sql, (name,))
    return result is not None

def commit():
    global db;
    db.commit()

def count_table(table_name):
    sql = "SELECT count(*) from %s"%table_name
    result = execute_one(sql)
    return result[0]

def create_table(table_name, **kwargs):
    field_arg = []
    for f_name in kwargs:
        f_type = kwargs[f_name]
        field_dec = "'%s' %s"%(f_name, f_type)
        field_arg.append(field_dec)

    sql = "create table '%s' ("%table_name
    sql += ', '.join(field_arg)
    sql += ')'

    execute_one(sql) 
