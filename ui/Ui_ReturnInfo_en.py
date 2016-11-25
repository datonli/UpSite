# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace\UpSite\ui\ReturnInfo_en.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_returnInfoDialog(object):
    def setupUi(self, returnInfoDialog):
        returnInfoDialog.setObjectName(_fromUtf8("returnInfoDialog"))
        returnInfoDialog.resize(400, 300)
        self.okButton = QtGui.QPushButton(returnInfoDialog)
        self.okButton.setGeometry(QtCore.QRect(160, 230, 75, 23))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.result = QtGui.QLabel(returnInfoDialog)
        self.result.setGeometry(QtCore.QRect(30, 30, 331, 181))
        self.result.setText(_fromUtf8(""))
        self.result.setAlignment(QtCore.Qt.AlignCenter)
        self.result.setObjectName(_fromUtf8("result"))

        self.retranslateUi(returnInfoDialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), returnInfoDialog.close)
        QtCore.QMetaObject.connectSlotsByName(returnInfoDialog)

    def retranslateUi(self, returnInfoDialog):
        returnInfoDialog.setWindowTitle(_translate("returnInfoDialog", "Return Information", None))
        self.okButton.setText(_translate("returnInfoDialog", "OK", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    returnInfoDialog = QtGui.QDialog()
    ui = Ui_returnInfoDialog()
    ui.setupUi(returnInfoDialog)
    returnInfoDialog.show()
    sys.exit(app.exec_())

