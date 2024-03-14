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
            raise Exception(f"isTableExist -> {er}")

    def createTable(self):
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
            if not self.isTableExist():
                raise Exception(f"failed to create table in database.")
        except Exception as er:
            raise Exception(f"createTable -> {er}")

    def readAllRows(self) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM accounts;""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not read database.\n")
            return ls
        except Exception as er:
            raise Exception(f"readAllRows -> {er}")

    def readColumnAllRows(self, columnName) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT {columnName} FROM accounts;""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not find '{columnName}' data in database.\n")
            return ls
        except Exception as er:
            raise Exception(f"readColumnAllRows -> {er}")

    def readColumn(self, columnName, condition):
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT {columnName} FROM accounts WHERE ADR = ?""", (condition,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not find data in database.\nwhere '{columnName} = {condition}.")
            return ls
        except Exception as er:
            raise Exception(f"readColumn -> {er}")

    def isExist(self, columnName: str, columnValue: str) -> bool:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM accounts WHERE {columnName} = ?", (columnValue,))
            data = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(data) > 0:
                return True
            else:
                return False
        except Exception as er:
            raise Exception(f"isExist -> {er}")

    def insertRow(self, acc: dict):
        try:
            if self.isExist('ADR', acc['address']):
                raise Exception(f"'{acc['address']}'\nis already exist in database.")
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
            if cursor.rowcount <= 0:
                raise Exception(f"inserting '{acc['address']}' data to database failed.")
        except Exception as er:
            raise Exception(f"insertRow -> {er}")

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
            raise Exception(f"isAccountExist -> {er}")

    def updateRowValue(self, columnName: str, newValue: str, address: str):
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE accounts SET {columnName} = '{newValue}' WHERE ADR = ?""", (address,))
            connection.commit()
            connection.close()
            if cursor.rowcount <= 0:
                self.readRow(address)
        except Exception as er:
            raise Exception(f"updateRowValue -> {er}")

    def readRow(self, address: str) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM accounts WHERE ADR = ?""", (address,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not find '{address}' data in database.")
            return ls
        except Exception as er:
            raise Exception(f"readRow -> {er}")

    def deleteRow(self, address: str):
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""DELETE from accounts WHERE ADR = ?""", (address,))
            connection.commit()
            connection.close()
            if cursor.rowcount <= 0:
                self.readRow(address)
        except Exception as er:
            raise Exception(f"deleteRow -> {er}")
