from sqlite3 import connect
from src import values, dataTypes


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
            table = f"""CREATE TABLE IF NOT EXISTS {values.TABLE_ACCOUNT} (
            {dataTypes.ACCOUNT.NAME.value} VARCHAR(255), 
            {dataTypes.ACCOUNT.ADDRESS.value} VARCHAR(255) NOT NULL,
            {dataTypes.ACCOUNT.ENTROPY.value} VARCHAR(255) NOT NULL,
            {dataTypes.ACCOUNT.PRIVATE_KEY.value} VARCHAR(255) NOT NULL,
            {dataTypes.ACCOUNT.PUBLIC_KEY_X.value} VARCHAR(255) NOT NULL,
            {dataTypes.ACCOUNT.PUBLIC_KEY_Y.value} VARCHAR(255) NOT NULL,
            {dataTypes.ACCOUNT.PUBLIC_KEY.value} VARCHAR(255) NOT NULL,
            {dataTypes.ACCOUNT.MNEMONIC.value} TEXT NOT NULL);"""
            cursor.execute(table)
            connection.commit()
            connection.close()
            if not self.isTableExist(values.TABLE_ACCOUNT):
                raise Exception(f"failed to create table in database.")
            else:
                print(f"create the table {values.TABLE_ACCOUNT} successfully")
        except Exception as er:
            raise Exception(f"createTableAccounts -> {er}")

    def insertAccountRow(self, acc: dict):
        try:
            if self.isExist(values.TABLE_ACCOUNT, dataTypes.ACCOUNT.ADDRESS.value, acc['address']):
                raise Exception(f"'{acc['address']}'\nis already exist in database.")
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {values.TABLE_ACCOUNT} ("
                f"{dataTypes.ACCOUNT.NAME.value}, "
                f"{dataTypes.ACCOUNT.ADDRESS.value}, "
                f"{dataTypes.ACCOUNT.ENTROPY.value}, "
                f"{dataTypes.ACCOUNT.PRIVATE_KEY.value}, "
                f"{dataTypes.ACCOUNT.PUBLIC_KEY_X.value}, "
                f"{dataTypes.ACCOUNT.PUBLIC_KEY_Y.value}, "
                f"{dataTypes.ACCOUNT.PUBLIC_KEY.value}, "
                f"{dataTypes.ACCOUNT.MNEMONIC.value}) "
                f"VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                (
                    str(acc['name']),
                    str(acc['address']),
                    str(acc['entropy']),
                    str(acc['privateKey']),
                    str(acc['publicKeyCoordinate'][0]),
                    str(acc['publicKeyCoordinate'][1]),
                    str(acc['publicKey']),
                    str(acc['mnemonic'])
                )
            )
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
            table = f"""CREATE TABLE IF NOT EXISTS {values.TABLE_TOKEN} (
                    {dataTypes.TOKEN.NAME.value} CHARACTER(20) NOT NULL, 
                    {dataTypes.TOKEN.ADDRESS.value} VARCHAR(255) NOT NULL, 
                    {dataTypes.TOKEN.SYMBOL.value} CHARACTER(20) NOT NULL, 
                    {dataTypes.TOKEN.TYPE.value} CHARACTER(20) NOT NULL, 
                    {dataTypes.TOKEN.DECIMALS.value} INT NOT NULL, 
                    {dataTypes.TOKEN.FAVORITE.value} BOOLEAN NOT NULL,
                    {dataTypes.TOKEN.LOGO.value} TEXT NOT NULL,                  
                    {dataTypes.TOKEN.ABI.value} BLOB NOT NULL);"""
            cursor.execute(table)
            connection.commit()
            connection.close()
            if not self.isTableExist(values.TABLE_TOKEN):
                raise Exception(f"failed to create table in database.")
            else:
                print(f"create the table {values.TABLE_TOKEN} successfully")
        except Exception as er:
            raise Exception(f"createTableTokens -> {er}")

    def insertTokenRow(self, token: dict) -> int:
        try:
            if self.isExist(values.TABLE_TOKEN, dataTypes.TOKEN.ADDRESS.value, token['data']['address']):
                # delete if exist to update data
                self.deleteRow(values.TABLE_TOKEN, dataTypes.TOKEN.ADDRESS.value, token['data']['address'])
                print(f"the old '{token['symbol']}' data was removed. new data will be replaced.")
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {values.TABLE_TOKEN} ("
                f"{dataTypes.TOKEN.NAME.value}, "
                f"{dataTypes.TOKEN.ADDRESS.value}, "
                f"{dataTypes.TOKEN.SYMBOL.value}, "
                f"{dataTypes.TOKEN.TYPE.value}, "
                f"{dataTypes.TOKEN.DECIMALS.value}, "
                f"{dataTypes.TOKEN.FAVORITE.value}, "
                f"{dataTypes.TOKEN.LOGO.value}, "
                f"{dataTypes.TOKEN.ABI.value})"
                f"VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                (
                    str(token['data']['name']),
                    str(token['data']['address']),
                    str(token['symbol']),
                    str(token['data']['type']),
                    int(token['data']['decimals']),
                    bool(token['favorite']),
                    str(token['data']['logoURI']),
                    str(token['data']['abi'])
                )
            )
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

    def readRow(self, tableName: str, condition: str, conditionVal: str) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM {tableName} WHERE {condition} = ?""",
                           (conditionVal,))
            ls = cursor.fetchall()
            connection.commit()
            connection.close()
            if len(ls) <= 0:
                raise Exception(f"can not find '{condition}' data in database.")
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
                self.readRow(tableName, condition, conditionVal)
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
                self.readRow(tableName, condition, conditionVal)
        except Exception as er:
            raise Exception(f"deleteRow -> {er}")

    def getTableColumns(self, tableName) -> list:
        try:
            connection = connect(self.databaseName)
            cursor = connection.cursor()
            cursor = connection.execute(f"select * from {tableName}")
            return list(map(lambda x: x[0], cursor.description))
        except Exception as er:
            raise Exception(f"getTableColumns -> {er}")
