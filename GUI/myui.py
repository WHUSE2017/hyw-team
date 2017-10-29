#coding: utf-8

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

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


class Ui_Form(QtGui.QDialog):
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

        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 80, 531, 321))


        self.retranslateUi(Form)
     #
     #    QtCore.QObject.connect(self.subplupbt, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.subfunc)
     # #   QtCore.QObject.connect(self.refreshpbt, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.refreshfunc)
     #    QtCore.QMetaObject.connectSlotsByName(Form)
     #    def subfunc(self):
     #        a=1


    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "追番查询", None))
        self.subplupbt.setText(_translate("Form", "添加订阅", None))
        self.refreshpbt.setText(_translate("Form", "重新抓取", None))
        # 初始化表格p
        self.table_set()
        #self.model.setItem(1, 3, QtGui.QStandardItem(_fromUtf8('456123')))
        self.adddata()



    def table_set(self):

        # 设置表格属性：
       # self.model.setRowCount(30)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(4)

        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels([_fromUtf8('番剧名称'), _fromUtf8('最新剧集'), _fromUtf8('上次观看'),_fromUtf8('操作')])
        #
        # self.tableWidget.setHeaderData(0, QtCore.Qt.Horizontal, _fromUtf8(u"番剧名称"))
        # self.tableWidget.setHeaderData(1, QtCore.Qt.Horizontal, _fromUtf8(u"最新剧集"))
        # self.tableWidget.setHeaderData(2, QtCore.Qt.Horizontal, _fromUtf8(u"上次观看"))
        # self.tableWidget.setHeaderData(3, QtCore.Qt.Horizontal, _fromUtf8(u"操作"))


        # 设置列宽
        self.tableWidget.setColumnWidth(0, 194)
        self.tableWidget.setColumnWidth(1, 105)
        self.tableWidget.setColumnWidth(2, 105)
        self.tableWidget.setColumnWidth(3, 110)


    def adddata(self):

        rsdata = ['975', '985', '866', [5,666666,777]]
        for row_number, row_data in enumerate(rsdata):
            self.tableWidget.insertRow(row_number)
            for i in range(len(row_data) + 1):
                if i < len(row_data):
                    self.tableWidget.setItem(row_number, i, QtGui.QTableWidgetItem(str(row_data[i])))
                # 添加按钮
                if i == len(row_data):
                    # 传入当前id
                    self.tableWidget.setCellWidget(row_number, i, self.buttonForRow(str(row_data[0])))

# 列表内添加按钮
    def buttonForRow(self,id):
        widget=QWidget()
        # 修改
        deleteBtn = QPushButton(_fromUtf8('删除'))
        deleteBtn.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')

        deleteBtn.clicked.connect(lambda:self.updateTable(id))

        hLayout = QHBoxLayout()
        hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(5,2,5,2)
        widget.setLayout(hLayout)
        return widget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
