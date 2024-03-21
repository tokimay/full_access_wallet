from sqlite3 import connect

from src.dataTypes import TOKENS
from src.values import TABLE_ACCOUNT, TABLE_TOKEN


class SQLITE:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        pass

    def initializeNew(self):
        self.createTableAccounts()
        self.createTableTokens()

    def isTableExist(self, tableName: str) -> bool:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            listOfTables = cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';").fetchall()
            connection.commit()
            connection.close()
            if not listOfTables:
                return False
            else:
                return True
        except Exception as er:
            raise Exception(f"isTableExist -> {er}")

    def isTableEmpty(self, tableName: str) -> bool:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM {tableName};""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) > 0:
                return False
            else:
                return True
        except Exception as er:
            raise Exception(f"isTableEmpty -> {er}")

    def createTableAccounts(self):
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            table = f"""CREATE TABLE IF NOT EXISTS {TABLE_ACCOUNT} (
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
            connection.commit()
            connection.close()
            if not self.isTableExist(TABLE_ACCOUNT):
                raise Exception(f"failed to create table in database.")
        except Exception as er:
            raise Exception(f"createTableAccounts -> {er}")

    def insertAccountRow(self, acc: dict):
        try:
            if self.isExist(TABLE_ACCOUNT, 'ADR', acc['address']):
                raise Exception(f"'{acc['address']}'\nis already exist in database.")
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {TABLE_ACCOUNT}(ENT, PRV, PUK_COR_X, PUK_COR_Y, PUK, ADR, NEM, NAM) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    acc['entropy'],
                    acc['privateKey'],
                    str(acc['publicKeyCoordinate'][0]),
                    str(acc['publicKeyCoordinate'][1]),
                    acc['publicKey'],
                    acc['address'],
                    acc['mnemonic'],
                    acc['name']
                ))
            connection.commit()
            connection.close()
            if cursor.rowcount <= 0:
                raise Exception(f"inserting '{acc['address']}' data to database failed.")
        except Exception as er:
            raise Exception(f"insertAccountRow -> {er}")

    def createTableTokens(self):
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            table = (
                f"CREATE TABLE IF NOT EXISTS {TABLE_TOKEN} ("
                f"{TOKENS.SYMBOL.value} CHARACTER(20) NOT NULL,"
                f"{TOKENS.TYPE.value} CHARACTER(20) NOT NULL, "
                f"{TOKENS.NAME.value} CHARACTER(20) NOT NULL,"
                f"{TOKENS.DECIMALS.value} INT NOT NULL, "
                f"{TOKENS.ADDRESS.value} VARCHAR(255) NOT NULL,  "
                f"{TOKENS.LOGO.value} TEXT NOT NULL);"
            )
            cursor.execute(table)
            connection.commit()
            connection.close()
            if not self.isTableExist(TABLE_TOKEN):
                raise Exception(f"failed to create table in database.")
        except Exception as er:
            raise Exception(f"createTableTokens -> {er}")

    def insertTokenRow(self, token: dict) -> int:
        try:
            if self.isExist(TABLE_TOKEN, TOKENS.ADDRESS.value, token['data']['address']):
                # delete if exist to update data
                self.deleteRow(TABLE_TOKEN, TOKENS.ADDRESS.value, token['data']['address'])
                print(f"the old '{token['symbol']}' data was removed. new data will be replaced.")
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {TABLE_TOKEN}("
                f"{TOKENS.SYMBOL.value}, "
                f"{TOKENS.TYPE.value}, "
                f"{TOKENS.NAME.value}, "
                f"{TOKENS.DECIMALS.value},"
                f" {TOKENS.ADDRESS.value},"
                f" {TOKENS.LOGO.value}) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    token['symbol'],
                    token['data']['type'],
                    token['data']['name'],
                    int(token['data']['decimals']),
                    token['data']['address'],
                    token['data']['logoURI']
                ))
            connection.commit()
            connection.close()
            if cursor.rowcount <= 0:
                raise Exception(f"inserting '{token['symbol']}' data to database failed.")
            else:
                print(f"successfully add '{token['symbol']}' info to dataBase")
                return cursor.rowcount
        except Exception as er:
            raise Exception(f"insertTokenRow -> {er}")

    def readAllRows(self, tableName: str) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM {tableName};""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not read database.\n")
            return ls
        except Exception as er:
            raise Exception(f"readAllRows -> {er}")

    def readColumnAllRows(self, tableName: str, columnName: str) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT {columnName} FROM {tableName};""")
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not find '{columnName}' data in database.\n")
            return ls
        except Exception as er:
            raise Exception(f"readColumnAllRows -> {er}")

    def readColumn(self, tableName: str, columnName: str, condition: str, conditionVal: str) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT {columnName} FROM {tableName} WHERE {condition} = ?""",
                           (conditionVal,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not find data in database.\nwhere '{columnName} = {conditionVal}.")
            return ls
        except Exception as er:
            raise Exception(f"readColumn -> {er}")

    def readRow(self, tableName: str, address: str) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM {tableName} WHERE ADR = ?""", (address,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not find '{address}' data in database.")
            return ls
        except Exception as er:
            raise Exception(f"readRow -> {er}")

    def isExist(self, tableName: str, columnName: str, columnValue: str) -> bool:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {tableName} WHERE {columnName} = ?", (columnValue,))
            data = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(data) > 0:
                return True
            else:
                return False
        except Exception as er:
            raise Exception(f"isExist -> {er}")

    def updateRowColumnValue(self, tableName: str, columnName: str, newValue: str, condition: str, conditionVal: str):
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE {tableName} SET {columnName} = '{newValue}' WHERE {condition} = ?""",
                           (conditionVal,))
            connection.commit()
            connection.close()
            if cursor.rowcount <= 0:  # delete nothing, if row is not exist will raise exception
                self.readRow(tableName, conditionVal)
        except Exception as er:
            raise Exception(f"updateRowColumnValue -> {er}")

    def deleteRow(self, tableName: str, condition: str, conditionVal: str):
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""DELETE from {tableName} WHERE {condition} = ?""", (conditionVal,))
            connection.commit()
            connection.close()
            if cursor.rowcount <= 0:  # delete nothing, if row is not exist will raise exception
                self.readRow(tableName, conditionVal)
        except Exception as er:
            raise Exception(f"deleteRow -> {er}")
