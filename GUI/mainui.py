# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui  import *

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(571, 442)
        self.searchbox = QtGui.QTextEdit(Form)
        self.searchbox.setGeometry(QtCore.QRect(20, 20, 371, 41))
        self.searchbox.setObjectName(_fromUtf8("searchbox"))
        self.subplupbt = QtGui.QPushButton(Form)
        self.subplupbt.setGeometry(QtCore.QRect(400, 20, 71, 41))
        self.subplupbt.setObjectName(_fromUtf8("subplupbt"))
        self.refreshpbt = QtGui.QPushButton(Form)
        self.refreshpbt.setGeometry(QtCore.QRect(480, 20, 71, 41))
        self.refreshpbt.setObjectName(_fromUtf8("refreshpbt"))
        self.subbox = QtGui.QTableWidget(Form)
        self.subbox.setGeometry(QtCore.QRect(20, 80, 531, 321))
        self.subbox.setObjectName(_fromUtf8("subbox"))
        self.subbox.setColumnCount(4)
        self.subbox.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.subbox.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.subbox.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.subbox.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.subbox.setHorizontalHeaderItem(3, item)
        newItem = QTableWidgetItem("666")
        self.subbox.setItem(newItem,0,0)



        self.retranslateUi(Form)
        QtCore.QObject.connect(self.subplupbt, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.subfunc)
        QtCore.QObject.connect(self.refreshpbt, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.refreshfunc)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.subplupbt.setText(_translate("Form", "添加订阅", None))
        self.refreshpbt.setText(_translate("Form", "刷新", None))
        item = self.subbox.horizontalHeaderItem(0)
        item.setText(_translate("Form", "番剧名称", None))
        item = self.subbox.horizontalHeaderItem(1)
        item.setText(_translate("Form", "当前最新集数", None))
        item = self.subbox.horizontalHeaderItem(2)
        item.setText(_translate("Form", "上次看到", None))
        item = self.subbox.horizontalHeaderItem(3)
        item.setText(_translate("Form", "操作", None))



