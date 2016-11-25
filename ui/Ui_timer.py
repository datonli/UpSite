# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace\UpSite\ui\timer.ui'
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

class Ui_calibrationClockDialog(object):
    def setupUi(self, calibrationClockDialog):
        calibrationClockDialog.setObjectName(_fromUtf8("calibrationClockDialog"))
        calibrationClockDialog.resize(400, 300)
        self.actualTime = QtGui.QDateTimeEdit(calibrationClockDialog)
        self.actualTime.setGeometry(QtCore.QRect(140, 110, 194, 22))
        self.actualTime.setMaximumTime(QtCore.QTime(23, 59, 59))
        self.actualTime.setCurrentSection(QtGui.QDateTimeEdit.YearSection)
        self.actualTime.setObjectName(_fromUtf8("actualTime"))
        self.setTimerButton = QtGui.QPushButton(calibrationClockDialog)
        self.setTimerButton.setGeometry(QtCore.QRect(150, 190, 75, 23))
        self.setTimerButton.setObjectName(_fromUtf8("setTimerButton"))
        self.cancelTimerButton = QtGui.QPushButton(calibrationClockDialog)
        self.cancelTimerButton.setGeometry(QtCore.QRect(240, 190, 75, 23))
        self.cancelTimerButton.setObjectName(_fromUtf8("cancelTimerButton"))
        self.label = QtGui.QLabel(calibrationClockDialog)
        self.label.setGeometry(QtCore.QRect(60, 110, 71, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.downSiteTime = QtGui.QDateTimeEdit(calibrationClockDialog)
        self.downSiteTime.setGeometry(QtCore.QRect(140, 60, 194, 22))
        self.downSiteTime.setObjectName(_fromUtf8("downSiteTime"))
        self.label_2 = QtGui.QLabel(calibrationClockDialog)
        self.label_2.setGeometry(QtCore.QRect(60, 60, 81, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(calibrationClockDialog)
        QtCore.QObject.connect(self.cancelTimerButton, QtCore.SIGNAL(_fromUtf8("clicked()")), calibrationClockDialog.close)
        QtCore.QMetaObject.connectSlotsByName(calibrationClockDialog)

    def retranslateUi(self, calibrationClockDialog):
        calibrationClockDialog.setWindowTitle(_translate("calibrationClockDialog", "时钟", None))
        self.actualTime.setDisplayFormat(_translate("calibrationClockDialog", "yyyy/MM/dd HH:mm:ss", None))
        self.setTimerButton.setText(_translate("calibrationClockDialog", "确定", None))
        self.cancelTimerButton.setText(_translate("calibrationClockDialog", "取消", None))
        self.label.setText(_translate("calibrationClockDialog", "校准时间", None))
        self.downSiteTime.setDisplayFormat(_translate("calibrationClockDialog", "yyyy/MM/dd HH:mm:ss", None))
        self.label_2.setText(_translate("calibrationClockDialog", "仪表时间", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    calibrationClockDialog = QtGui.QDialog()
    ui = Ui_calibrationClockDialog()
    ui.setupUi(calibrationClockDialog)
    calibrationClockDialog.show()
    sys.exit(app.exec_())

