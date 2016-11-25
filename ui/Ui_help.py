# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace\UpSite\ui\help.ui'
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
        HelpDialog.setWindowTitle(_translate("HelpDialog", "操作说明", None))
        self.label.setText(_translate("HelpDialog", "本软件使用简单，操作人性化。下面是操作说明。\n"
"窗口简单，主要分为三大模块：\n"
"1.基本信息；\n"
"2.文件操作；\n"
"3.记录查询。\n"
"\n"
"基本查询中实现了两大功能——实时显示和设置参数相关。\n"
"文件操作中主要包含了链接下位机，读取下位机中文件情况，并能够接收、删除等操作。\n"
"记录查询是主要的信息显示模块。在将下位机导入到PC之后，在文件管理目录下能够直接找到该文件，导入文件到窗口中可以看到该文件的数据表格和曲线图，并能够进行记录查询。", None))

import UpSite_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    HelpDialog = QtGui.QDialog()
    ui = Ui_HelpDialog()
    ui.setupUi(HelpDialog)
    HelpDialog.show()
    sys.exit(app.exec_())

