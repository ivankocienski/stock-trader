
import sqlite3

db = None

def _sql_trace(sql):
    print("SQL: %s"%sql)

def init(path, debug=False): 
    global db
    print("using database '%s'"%path)
    db = sqlite3.connect(path)
    if debug:
        db.set_trace_callback(_sql_trace)

def execute_one(sql, args=()):
    global db
    cur = db.cursor()
    cur.execute(sql, args)
    return cur.fetchone()

def execute_id(sql, args=()):
    global db
    cur = db.cursor()
    cur.execute(sql, args) 
    return cur.lastrowid

def execute(sql, args=()):
    global db
    cur = db.cursor()
    return cur.execute(sql, args)

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
