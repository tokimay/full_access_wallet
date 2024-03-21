from PyQt6.QtWidgets import QProgressBar, QDialog, QVBoxLayout, QListWidget
from src import network
from src.dataTypes import TOKENS
from src.system import errorSignal
from src.threads import AddTokenToDataBase
from src.values import TABLE_TOKEN


class AddTokens(QDialog):
    def __init__(self, db):
        try:
            super(AddTokens, self).__init__()
            tokens = network.getTokenList()
            self.count = len(tokens['list'])
            self.setWindowTitle('Syncing tokens list..')
            self.progress = QProgressBar(self)
            self.progress.setValue(0)
            self.resize(300, 400)
            self.progress.resize(300, 50)
            self.vbox = QVBoxLayout()
            self.listWidget = QListWidget()
            self.listWidget.resize(300, 350)
            self.vbox.addWidget(self.progress)
            self.vbox.addWidget(self.listWidget)
            self.setLayout(self.vbox)
            self.progress.setMaximum(self.count)
            self.thread = AddTokenToDataBase(db, tokens, self.listWidget)
            self.thread.signalData.connect(self.signalAccept)
            self.thread.error.connect(self.exception)
            self.thread.start()
        except Exception as er:
            errorSignal.newError.emit(f"AddTokens -> __init__ -> {str(er)}")

    def signalAccept(self, msg):
        try:
            print('emit = ', msg, ' ', type(msg))
            if msg == self.count:
                print('pppppppppppppp')
                self.endProgress()
            else:
                self.progress.setValue(int(msg))
        except Exception as er:
            errorSignal.newError.emit(f"AddTokens -> signal_accept -> {str(er)}")

    def endProgress(self):
        try:
            print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            self.close()
        except Exception as er:
            errorSignal.newError.emit(f"AddTokens -> endProgress -> {str(er)}")

    def exception(self, message):
        self.thread.terminate()
        errorSignal.newError.emit(f"AddTokens -> __init__ -> {message}")

    def closeEvent(self, evnt):
        self.thread.terminate()


def readTokens(db):
    tokens = db.readAllRows(TABLE_TOKEN)
    result = []
    for token in tokens:
        d = {
            TOKENS.SYMBOL.value: token[0],
            TOKENS.TYPE.value: token[1],
            TOKENS.NAME.value: token[2],
            TOKENS.DECIMALS.value: token[3],
            TOKENS.ADDRESS.value: token[4],
            TOKENS.LOGO.value: token[5]
        }
        result.append(d)
    for r in result:
        print(r)
    print(len(result))

