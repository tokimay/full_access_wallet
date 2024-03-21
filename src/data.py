from PyQt6.QtWidgets import QProgressBar, QDialog, QVBoxLayout, QListWidget
from src import network, dataTypes, system, threads, values


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
            self.thread = threads.AddTokenToDataBase(db, tokens, self.listWidget)
            self.thread.signalData.connect(self.signalAccept)
            self.thread.error.connect(self.exception)
            self.thread.start()
        except Exception as er:
            system.errorSignal.newError.emit(f"AddTokens -> __init__ -> {str(er)}")

    def signalAccept(self, msg):
        try:
            if msg == self.count:
                self.endProgress()
            else:
                self.progress.setValue(int(msg))
        except Exception as er:
            system.errorSignal.newError.emit(f"AddTokens -> signal_accept -> {str(er)}")

    def endProgress(self):
        try:
            self.close()
        except Exception as er:
            system.errorSignal.newError.emit(f"AddTokens -> endProgress -> {str(er)}")

    def exception(self, message):
        self.thread.terminate()
        system.errorSignal.newError.emit(f"AddTokens -> __init__ -> {message}")

    def closeEvent(self, evnt):
        self.thread.terminate()


def readTokens(db) -> list:
    try:
        tokens = db.readAllRows(values.TABLE_TOKEN)
        result = []
        for token in tokens:
            d = {
                dataTypes.TOKEN.NAME.value: token[0],
                dataTypes.TOKEN.ADDRESS.value: token[1],
                dataTypes.TOKEN.SYMBOL.value: token[2],
                dataTypes.TOKEN.TYPE.value: token[3],
                dataTypes.TOKEN.DECIMALS.value: token[4],
                dataTypes.TOKEN.LOGO.value: token[5],
                dataTypes.TOKEN.ABI.value: token[6]
            }
            result.append(d)
        return result
    except Exception as er:
        raise Exception(f"readTokens -> {er}")
