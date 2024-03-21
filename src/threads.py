from time import sleep
from PyQt6.QtCore import QThread, pyqtSignal


class GetBalance(QThread):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def run(self):
        while True:
            sleep(5)
            self.window.getBalance()


class AddTokenToDataBase(QThread):
    signalData = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, db, tokens, listWidget):
        try:
            super(AddTokenToDataBase, self).__init__()
            self.db = db
            self.tokens = tokens
            self.listWidget = listWidget
        except Exception as er:
            self.error.emit(f"__init__:Thread -> {er}")

    def __del__(self):
        try:
            self.wait()
        except Exception as er:
            self.error.emit(f"__del__:Thread -> {er}")

    def run(self):
        try:
            count = len(self.tokens['list'])
            i = 1
            for tok in self.tokens['list']:
                res = self.db.insertTokenRow(tok)
                self.listWidget.addItem(f"successfully add '{tok['symbol']}' info to dataBase")
                self.listWidget.scrollToBottom()
                self.signalData.emit(i)
                i = i + res
            print('i-1 = ', i-1, 'count = ', count)
            if i-1 == count:
                self.signalData.emit(count)
            else:
                raise Exception(f"cursor.rowcount:{i} != count:{count}")
        except Exception as er:
            self.error.emit(f"AddTokenToDataBase:Thread -> {er}")
