import sqlite3

from src import gui_errorDialog


class Sqlite:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        pass

    def isTableExist(self) -> bool:
        try:
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
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return False

    def isAccountExist(self) -> bool:
        try:
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
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return False

    def createTable(self):
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()
            table = """CREATE TABLE IF NOT EXISTS accounts (
                        ENT VARCHAR(255) NOT NULL,
                        PRV VARCHAR(255) NOT NULL,
                        PUK_COR_X VARCHAR(255) NOT NULL,
                        PUK_COR_Y VARCHAR(255) NOT NULL,
                        PUK VARCHAR(255) NOT NULL,
                        ADR VARCHAR(255) NOT NULL,
                        NEM TEXT NOT NULL
                                        );"""
            cursor.execute(table)
            print('cursor last row id:', cursor.lastrowid)
            connection.commit()
            connection.close()
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()

    def insertRow(self, acc: dict):
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO accounts(ENT, PRV, PUK_COR_X, PUK_COR_Y, PUK, ADR, NEM) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    acc['entropy'],
                    acc['privateKey'],
                    str(acc['publicKeyCoordinate'][0]),
                    str(acc['publicKeyCoordinate'][1]),
                    acc['publicKey'],
                    acc['address'],
                    acc['mnemonic']
                ))
            connection.commit()
            connection.close()
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()

    def readAllRows(self) -> list:
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM accounts;""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            return ls
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return []

    def readColumn(self, columnName) -> list:
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute("""SELECT """ + columnName.value + """ FROM accounts;""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            return ls
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return []

    def readColumnByCondition(self, columnName, condition) -> list:
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute("""SELECT """ + columnName.value + """ FROM accounts WHERE ADR = ?""", (condition,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            return ls
        except Exception as er:
            gui_errorDialog.Error(str(er)).exec()
            return []
