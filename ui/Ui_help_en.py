# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace\UpSite\ui\help_en.ui'
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

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        HelpDialog.setObjectName(_fromUtf8("HelpDialog"))
        HelpDialog.resize(437, 464)
        self.verticalLayout = QtGui.QVBoxLayout(HelpDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(HelpDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(HelpDialog)
        QtCore.QMetaObject.connectSlotsByName(HelpDialog)

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(_translate("HelpDialog", "Operation Information", None))
        self.label.setText(_translate("HelpDialog", "The software is simple to use and user-friendly operation The following is a description of the operation.\n"
"The window is simple, mainly divided into three modules:\n"
"1 Basic information;\n"
"2 file operation;\n"
"3 record query.\n"
"The basic query achieves two functions: real-time display and set the relevant parameters\n"
"File operations mainly include the link to the next bit machine, read the next bit machine file, and be able to receive, delete and other operations.\n"
"Record query is the main information display module. In the next bit machine into the PC, in the file management directory can directly find the file, import the file into the window can see the file data tables and graphs, and can record query.", None))

import UpSite_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    HelpDialog = QtGui.QDialog()
    ui = Ui_HelpDialog()
    ui.setupUi(HelpDialog)
    HelpDialog.show()
    sys.exit(app.exec_())

