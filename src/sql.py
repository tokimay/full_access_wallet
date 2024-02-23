import sqlite3

tableName = 'accounts'


def sqlInit():
    con = sqlite3.connect('data')
    con.close()


def isTableExist():
    con = sqlite3.connect('data')
    cur = con.cursor()
    listOfTables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='accounts';").fetchall()
    con.close()
    if not listOfTables:
        return False
    else:
        return True


def createTable():
    con = sqlite3.connect('data')
    cur = con.cursor()
    table = """ CREATE TABLE accounts(
                entropy VARCHAR(255),
                privateKey VARCHAR(255),
                publicKey TEXT,
                address NCHAR(42)
            ); """
    cur.execute(table)
    con.close()
