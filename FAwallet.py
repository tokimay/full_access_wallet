from PyQt6.QtWidgets import QApplication
from sys import argv
from src import values, threads, database, dataTypes, data
from src.GUI import gui_error, gui_mainWindow, gui_userChoice, gui_message, gui_processBar

APP = QApplication(argv)


db = database.SQLITE(values.DB_NAME)
getBalance = False

try:
    db.initializeNew()
    if db.isTableEmpty(values.TABLE_TOKEN):
        gui_processBar.AddTokensToDatabase(db).exec()
except Exception as er:
    gui_error.WINDOW('FAwallet', str(er)).exec()
    exit()
window = gui_mainWindow.Ui(values.DB_NAME)
window.show()


try:
    if getBalance:
        balanceThread = threads.GetBalance(window)
        balanceThread.finished.connect(APP.exit)
        balanceThread.start()
except Exception as er:
    gui_error.WINDOW('FAwallet', str(er)).exec()
    exit()

APP.exec()
