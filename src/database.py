import sqlite3


class Sqlite:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        pass

    def isTableExist(self):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        listOfTables = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='accounts';").fetchall()
        connection.commit()
        connection.close()
        if not listOfTables:
            return False
        else:
            return True

    def isAccountExist(self):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM accounts;""")
        ls = cursor.fetchall()
        connection.commit()
        connection.close()
        if len(ls) > 0:
            return True
        else:
            return False

    def createTable(self):
        table = """CREATE TABLE IF NOT EXISTS accounts (
                    ENT VARCHAR(255) NOT NULL,
                    PRV VARCHAR(255) NOT NULL,
                    PUK_COR_X VARCHAR(255) NOT NULL,
                    PUK_COR_Y VARCHAR(255) NOT NULL,
                    PUK VARCHAR(255) NOT NULL,
                    ADR VARCHAR(255) NOT NULL
                                    );"""
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        cursor.execute(table)
        print('cursor last row id:', cursor.lastrowid)
        connection.commit()
        connection.close()

    def insertRow(self, acc: dict):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO accounts(ENT, PRV, PUK_COR_X, PUK_COR_Y, PUK, ADR) VALUES (?, ?, ?, ?, ?, ?)",
                       (
                           bin(acc['privateKey'])[2:].zfill(256),
                           hex(acc['privateKey']),
                           hex(acc['publicKeyCoordinate'][0]),
                           hex(acc['publicKeyCoordinate'][1]),
                           hex(acc['publicKey']),
                           hex(acc['address'])
                       ))
        connection.commit()
        connection.close()

    def readAllRows(self):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM accounts;""")
        ls = cursor.fetchall()
        connection.commit()
        connection.close()
        return ls

    def readColumn(self, columnName):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        cursor.execute("""SELECT """ + columnName.value + """ FROM accounts;""")
        ls = cursor.fetchall()
        connection.commit()
        connection.close()
        return ls

    def readColumnByCondition(self, columnName, condition):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        cursor.execute("""SELECT """ + columnName.value + """ FROM accounts WHERE ADR = ?""", (condition,))
        ls = cursor.fetchall()
        connection.commit()
        connection.close()
        return ls
