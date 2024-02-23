from PyQt6 import QtWidgets


class MouseTracker(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.entropy = ''
        self.addNew = True
        self.eventSelector = True
        self.size = 256

    def initUI(self):
        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle('Mouse Tracker')

    def mouseMoveEvent(self, event):
        if len(self.entropy) > (self.size + 1024):
            self.entropy = self.entropy[512:(self.size + 512)]
            self.addNew = False
            self.setWindowTitle('100% Done close the window now')
            self.close()
        else:
            if self.addNew:
                if len(self.entropy) > 1024:
                    self.setWindowTitle(
                        '({} : {}) {}%'.format(
                            event.scenePosition().x(),
                            event.scenePosition().y(),
                            int(((len(self.entropy) - 1024) * 100) / self.size)
                        ))
                else:
                    self.setWindowTitle('move mouse in box randomly')
                if self.eventSelector:
                    self.entropy = self.entropy + bin(int(event.scenePosition().x()))[2:]
                    self.eventSelector = False
                else:
                    self.entropy = self.entropy + bin(int(event.scenePosition().y()))[2:]
                    self.eventSelector = True

    def getEntropy(self):
        return self.entropy
