from time import sleep
from PyQt6.QtCore import QThread, pyqtSignal
from time import gmtime, strftime
from src import data, system


class GetBalance(QThread):
    ok = pyqtSignal(float, str)
    error = pyqtSignal(str)

    def __init__(self, coinData=None):
        try:
            super().__init__()
            self.coinData = coinData
        except Exception as er:
            # self.error.emit(f"__init__:Thread -> run -> {er}")
            self.error.emit(f"{er}")

    def setCoin(self, coinData):
        try:
            self.coinData = coinData
        except Exception as er:
            # self.error.emit(f"setCoin:Thread -> run -> {er}")
            self.error.emit(f"{er}")

    def run(self):
        while True:
            try:
                if self.coinData is not None:
                    balance, symbol = data.getCoinBalance(self.coinData)
                    self.ok.emit(balance, symbol)
                    sleep(5)
                else:
                    self.terminate()
            except Exception as er:
                # self.error.emit(f"GetBalance:Thread -> run -> {er}")
                self.error.emit(f"{er}")


class GetTokenBalance(QThread):
    end = pyqtSignal(list)

    def __init__(self, tokens: list, provider: str, address: str):
        super().__init__()
        self.tokens = tokens
        self.provider = provider
        self.address = address


class AddToken(QThread):
    signalData = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, db, tokens, listWidget):
        try:
            super(AddToken, self).__init__()
            self.db = db
            self.tokens = tokens
            self.listWidget = listWidget
        except Exception as er:
            self.error.emit(f"AddToken:Thread -> __init__ -> {er}")

    def __del__(self):
        try:
            self.wait()
        except Exception as er:
            self.error.emit(f"AddToken:Thread -> __del__ -> {er}")

    def run(self):
        try:
            count = len(self.tokens['list'])
            i = 1
            for tok in self.tokens['list']:
                if tok['symbol'] == 'ETH' or tok['symbol'] == 'USDT' or tok['data']['type'] == 'Sepolia':
                    tok['favorite'] = True
                else:
                    tok['favorite'] = False
                res = self.db.insertTokenRow(tok)
                self.listWidget.addItem(f"successfully add '{tok['symbol']}' info to dataBase")
                self.listWidget.scrollToBottom()
                self.signalData.emit(i)
                i = i + res
            print(f"{strftime('%H:%M:%S', gmtime())}:i-1 = ', i - 1, 'count = {count}")
            if i - 1 == count:
                self.signalData.emit(count)
            else:
                raise Exception(f"cursor.rowcount:{i} != count:{count}")
        except Exception as er:
            self.error.emit(f"AddToken:Thread -> run -> {er}")
