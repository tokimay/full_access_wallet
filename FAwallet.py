from PyQt6.QtWidgets import QApplication
from sys import argv
from src import values, database
from src.GUI import gui_error, gui_mainWindow, gui_processBar

APP = QApplication(argv)


db = database.SQLITE(values.DB_NAME)
try:
    db.initializeNew()
    if db.isTableEmpty(values.TABLE_TOKEN):
        gui_processBar.AddTokensToDatabase(db).exec()
except Exception as er:
    gui_error.WINDOW('FAwallet', str(er)).exec()
    exit()
window = gui_mainWindow.Ui(values.DB_NAME)
window.show()
APP.exec()
