# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MouseNow3.0.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
import sys
import pyautogui
import pyperclip
import keyboard

class appThread(QThread):
    """
    The thread for getting values so the gui wont hang
    """
    y_changed = pyqtSignal(int)
    x_changed = pyqtSignal(int)
    rgb_changed = pyqtSignal(tuple)

    def run(self):
        while True:
            rgbStr = ""
            try:
                x,y = pyautogui.position()
                rgb = pyautogui.screenshot().getpixel((x,y))
                self.x_changed.emit(x)
                self.y_changed.emit(y)
                self.rgb_changed.emit(rgb)
                if keyboard.is_pressed(' '):
                    for item in rgb:
                        rgbStr = rgbStr + str(item) + ','
                    pyperclip.copy("(" + str(x) + "," + str(y) + ")" + " rgb(" + rgbStr[:-1]+ ")")
                    print("Value copied to clipboard")
            except IndexError:
                print("Out of main monitor")


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.setEnabled(True)
        self.resize(294, 43)
        self.setMouseTracking(False)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setStatusTip("")
        self.setWhatsThis("")

        self.labelX = QtWidgets.QLabel(self)
        self.labelX.setGeometry(QtCore.QRect(10, 10, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelX.setFont(font)
        self.labelX.setObjectName("labelX")

        self.textEditX = QtWidgets.QTextEdit(self)
        self.textEditX.setGeometry(QtCore.QRect(30, 10, 41, 21))
        self.textEditX.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditX.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditX.setReadOnly(True)
        self.textEditX.setAcceptRichText(False)
        self.textEditX.setObjectName("textEditX")

        self.labelY = QtWidgets.QLabel(self)
        self.labelY.setGeometry(QtCore.QRect(80, 10, 31, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelY.setFont(font)
        self.labelY.setObjectName("labelY")

        self.textEditY = QtWidgets.QTextEdit(self)
        self.textEditY.setGeometry(QtCore.QRect(100, 10, 41, 21))
        self.textEditY.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditY.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditY.setObjectName("textEditY")

        self.labelRGB = QtWidgets.QLabel(self)
        self.labelRGB.setGeometry(QtCore.QRect(160, 10, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelRGB.setFont(font)
        self.labelRGB.setObjectName("labelRGB")

        self.textEditRGB = QtWidgets.QTextEdit(self)
        self.textEditRGB.setGeometry(QtCore.QRect(190, 10, 91, 21))
        self.textEditRGB.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditRGB.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEditRGB.setObjectName("textEditRGB")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()
        self.onProgramStart()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MouseNow"))
        self.labelX.setText(_translate("Dialog", " X:"))
        self.labelY.setText(_translate("Dialog", " Y:"))
        self.labelRGB.setText(_translate("Dialog", "RGB:"))

    def onProgramStart(self):
        self.valueThread = appThread()
        self.valueThread.x_changed.connect(self.changeX)
        self.valueThread.y_changed.connect(self.changeY)
        self.valueThread.rgb_changed.connect(self.changeRgb)
        self.valueThread.start()

    def changeX(self, value):
        self.textEditX.setText(str(value))

    def changeY(self,value):
        self.textEditY.setText(str(value))

    def changeRgb(self, value):
        self.textEditRGB.setText(str(value))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    sys.exit(app.exec_())

