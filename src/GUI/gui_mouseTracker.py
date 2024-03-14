from PyQt6.QtWidgets import QDialog


class WINDOW(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.entropy = ''
        self.addNew = True
        self.eventSelector = True
        self.size = 256
        self.setWindowTitle('Move mouse in box randomly')

    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Mouse Tracker')

    def mouseMoveEvent(self, event):
        div = 8192
        if len(self.entropy) > (div + self.size):
            self.entropy = self.entropy[int(div/2):int((div/2) + self.size)]
            self.addNew = False
            self.setWindowTitle('100% Done close the window now')
            self.close()
        else:
            if self.addNew:
                self.setWindowTitle(
                        '({} : {}) {}%'.format(
                            event.scenePosition().x(),
                            event.scenePosition().y(),
                            int(len(self.entropy * 100) / (div + self.size))
                        ))
                if self.eventSelector:
                    self.entropy = self.entropy + bin(int(event.scenePosition().x()))[2:]
                    self.eventSelector = False
                else:
                    self.entropy = self.entropy + bin(int(event.scenePosition().y()))[2:]
                    self.eventSelector = True

    def getEntropy(self):
        return self.entropy
