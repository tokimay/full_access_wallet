import sqlite3


class sqlite:
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

    def insertRow(self, row: list):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO accounts(ENT, PRV, PUK_COR_X, PUK_COR_Y, PUK, ADR) VALUES (?, ?, ?, ?, ?, ?)",
                            (row[0], row[1], row[2], row[3], row[4], row[5]))
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
        cursor.execute("""SELECT """ + columnName + """ FROM accounts;""")
        ls = cursor.fetchall()
        connection.commit()
        connection.close()
        return ls


