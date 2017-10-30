#-*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from simplejson import load
from spider import *


reload(sys)
sys.setdefaultencoding('utf-8')

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

        QtCore.QObject.connect(self.refreshpbt, QtCore.SIGNAL('clicked()'), self.seek)# 重新抓取触发seek
        QtCore.QObject.connect(self.subplupbt, QtCore.SIGNAL('clicked()'), self.addsublist)
        self.retranslateUi(Form)


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
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(5)
        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels([_fromUtf8('番剧名称'), _fromUtf8('最新剧集'), _fromUtf8('更新日'),_fromUtf8('观看地址'),_fromUtf8('操作')])
        # 设置列宽
        self.tableWidget.setColumnWidth(0, 194)
        self.tableWidget.setColumnWidth(1, 85)
        self.tableWidget.setColumnWidth(2, 70)
        self.tableWidget.setColumnWidth(3, 85)
        self.tableWidget.setColumnWidth(4, 80)



    # 根据sublist.txt抓取信息存放在cache/json里
    def seek(self):
        #getLastEpisode(url)
        with open("../cache/subscribe.json", "r") as dump_f:
            temp = load(dump_f)
            temp_num = temp['total']
            temp_con = temp['list']
            for row_number in range(temp_num):
                getLastEpisode(temp_con[row_number]['address'])

    # 添加订阅按钮
    def addsublist(self):
        subtext = self.searchbox.toPlainText()
        with open("sublist.txt", mode="a") as data:
            data.write('\n')
            data.write(subtext)

        subtext = str(subtext)
        subtext = subtext.encode('utf-8')
        search_bilibili(subtext)

    # table内添加数据
    def adddata(self):

        with open("../cache/subscribe.json", "r") as dump_f:
            temp = load(dump_f)
            temp_num = temp['total']
            temp_con = temp['list']

        for row_number in range(temp_num):
            self.tableWidget.insertRow(row_number)
            self.tableWidget.setItem(row_number, 0, QtGui.QTableWidgetItem((temp_con[row_number]['name'])))
            self.tableWidget.setItem(row_number, 1, QtGui.QTableWidgetItem(str(temp_con[row_number]['lastEpisode'])))
            self.tableWidget.setItem(row_number, 2, QtGui.QTableWidgetItem((temp_con[row_number]['updatetime'])))
            # self.tableWidget.setItem(row_number, 3, QtGui.QTableWidgetItem((temp_con[row_number]['address'])))
            # strr = '''<a style= "color:#55aaff; text-decoration:none; font-size:11pt; font-family:Consolas; font-weight: bold;" \
            # href="http://www.google.com">Open Url</a>'''

            strrr = '''<a style= "color:#55aaff; text-decoration:none; font-size:11pt; font-family:Consolas; font-weight: bold;" \ 
            href="''' + temp_con[row_number]['address'] + '''">(Open Url)</a>'''

            version = QLabel(strrr, self)
            version.setOpenExternalLinks(True)
            self.tableWidget.setCellWidget(row_number, 3, version)
            self.tableWidget.setCellWidget(row_number, 4, self.buttonForRow(temp_con[row_number]['name']))



    def buttonForRow(self,id):
        widget=QWidget()
        # 修改
        deleteBtn = QPushButton(_fromUtf8('移出订阅'))
        deleteBtn.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')

        deleteBtn.clicked.connect(lambda:self.removeLine(id))

        hLayout = QHBoxLayout()
        hLayout.addWidget(deleteBtn)
        hLayout.setContentsMargins(5,2,5,2)
        widget.setLayout(hLayout)
        return widget

    def removeLine(self, id):
        print (id)
        #id = unicode(id ,"utf-8")
        deleateSubscribeList(id)
        #self.retranslateUi(Form)  很迷很迷
        self.tableWidget.update()

'''
    def removeLine(self, linenom):
        line = int(linenom)
        filename = 'sublist.txt'
        fro = open(filename, "rb")

        current_line = 0
        while current_line < line:
            fro.readline()
            current_line += 1

        seekpoint = fro.tell()
        frw = open(filename, "r+b")
        frw.seek(seekpoint, 0)

        # read the line we want to discard
        fro.readline()

        # now move the rest of the lines in the file
        # one line back
        chars = fro.readline()
        while chars:
            frw.writelines(chars)
            chars = fro.readline()

        fro.close()
        frw.truncate()
        frw.close()
'''

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
