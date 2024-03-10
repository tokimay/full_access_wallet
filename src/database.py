from src import gui_errorDialog
from sqlite3 import connect


class Sqlite:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        pass

    def isTableExist(self) -> bool:
        try:
            connection = connect(self.databaseName)
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
            gui_errorDialog.Error('isTableExist', str(er)).exec()
            return False

    def isAccountExist(self) -> bool:
        try:
            connection = connect(self.databaseName)
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
            gui_errorDialog.Error('isAccountExist', str(er)).exec()
            return False

    def isRowExist(self, name: str, value: str) -> bool:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM accounts WHERE {name} = ?", (value,))
            data = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(data) == 0:
                return False
            else:
                return True
        except Exception as er:
            gui_errorDialog.Error('isRowExist', str(er)).exec()
            return False

    def createTable(self) -> bool:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            table = """CREATE TABLE IF NOT EXISTS accounts (
                        ENT VARCHAR(255) NOT NULL,
                        PRV VARCHAR(255) NOT NULL,
                        PUK_COR_X VARCHAR(255) NOT NULL,
                        PUK_COR_Y VARCHAR(255) NOT NULL,
                        PUK VARCHAR(255) NOT NULL,
                        ADR VARCHAR(255) NOT NULL,
                        NEM TEXT NOT NULL,
                        NAM VARCHAR(255)
                                        );"""
            cursor.execute(table)
            print('cursor last row id:', cursor.lastrowid)
            connection.commit()
            connection.close()
            return True
        except Exception as er:
            gui_errorDialog.Error('createTable', str(er)).exec()
            return False

    def insertRow(self, acc: dict) -> bool:
        try:
            existAccount = self.isRowExist('ADR', acc['address'])
            if existAccount:
                gui_errorDialog.Error('insertRow', 'This account is already exist.\n').exec()
                return False
            else:
                connection = connect(self.databaseName)
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO accounts(ENT, PRV, PUK_COR_X, PUK_COR_Y, PUK, ADR, NEM, NAM) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        acc['entropy'],
                        acc['privateKey'],
                        str(acc['publicKeyCoordinate'][0]),
                        str(acc['publicKeyCoordinate'][1]),
                        acc['publicKey'],
                        acc['address'],
                        acc['mnemonic'],
                        'No name'
                    ))
                connection.commit()
                connection.close()
                return True
        except Exception as er:
            gui_errorDialog.Error('insertRow', str(er)).exec()
            return False

    def readAllRows(self) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM accounts;""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            return ls
        except Exception as er:
            gui_errorDialog.Error('readAllRows', str(er)).exec()
            return []

    def readRowByCondition(self, condition: str) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM accounts WHERE ADR = ?""", (condition,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            return ls
        except Exception as er:
            gui_errorDialog.Error('readRowByCondition', str(er)).exec()
            return []

    def readColumnAllRows(self, columnName) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT {columnName} FROM accounts;""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            return ls
        except Exception as er:
            gui_errorDialog.Error('readColumnAllRows', str(er)).exec()
            return []

    def readColumnByCondition(self, columnName, condition) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT {columnName} FROM accounts WHERE ADR = ?""", (condition,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            return ls
        except Exception as er:
            gui_errorDialog.Error('readColumnByCondition', str(er)).exec()
            return []

    def updateRowValue(self, columnName: str, newValue: str, condition: str) -> bool:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE accounts SET {columnName} = '{newValue}' WHERE ADR = ?""", (condition,))
            connection.commit()
            connection.close()
            return True
        except Exception as er:
            print('here')
            gui_errorDialog.Error('updateRowValue', str(er)).exec()
            return False
