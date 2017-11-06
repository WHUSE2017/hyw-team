#-*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from simplejson import load
from spider_changed import *

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

class SearchThread(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal()
    _signal = QtCore.pyqtSignal()
    def __init__(self,args):
        super(SearchThread,self).__init__()
        self.args = args


    def run(self):
        subtext = str(self.args)
        subtext = subtext.encode('utf-8')
        ans = add_list(subtext)
        if ans == 'NoSuch':
            print 'NoSuch'
            self._signal.connect(self.mySignal)
            self._signal.emit()

        self.finishSignal.emit()

    def mySignal(self):
        list_run = []
        dilogUi = warningBox(u"搜索失败",u"请输入番剧的全名。如‘奇诺之旅 新作’",list_run)
        if dilogUi.exec_():
            return


class SeekThread(QtCore.QThread):
    seekfinishSignal = QtCore.pyqtSignal()
    def __init__(self,args):
        super(SeekThread,self).__init__()
        self.args = args

    def run(self):
        Update()
        self.seekfinishSignal.emit()


class Ui_Form(QtGui.QDialog):
    def setupUi(self, Form):

        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(571, 442)
        self.searchbox = QtGui.QTextEdit(Form)
        self.searchbox.setGeometry(QtCore.QRect(20, 20, 371, 41))
        self.searchbox.setFont(QtGui.QFont("Microsoft YaHei", 12))
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
        self.subplupbt.setFont(QtGui.QFont("Microsoft YaHei", 11))
        self.refreshpbt.setText(_translate("Form", "更新剧集", None))
        self.refreshpbt.setFont(QtGui.QFont("Microsoft YaHei", 11))
        # 初始化表格
        self.table_set()
        self.adddata()

    def table_set(self):

        # 设置表格属性：
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(10)
        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels([_fromUtf8('番剧名称'), _fromUtf8('最新剧集'), _fromUtf8('版权站'),_fromUtf8('观看地址'),_fromUtf8('操作')])
        # 设置列宽
        self.tableWidget.setColumnWidth(0, 170)
        self.tableWidget.setColumnWidth(1, 85)
        self.tableWidget.setColumnWidth(2, 70)
        self.tableWidget.setColumnWidth(3, 85)
        self.tableWidget.setColumnWidth(4, 80)

    def seek(self):
        self.refreshpbt.setDisabled(True)
        self.seekthread = SeekThread('1')
        self.seekthread.seekfinishSignal.connect(self.refreshUI)
        self.seekthread.start()

    # 添加订阅按钮
    def addsublist(self):
        subtext = self.searchbox.toPlainText()
        if subtext == '':
            list_run = []
            dilogUi = warningBox(u"搜索失败", u"请输入番剧全名", list_run)
            if dilogUi.exec_():
                return
        else:
            self.subplupbt.setDisabled(True)
            self.searchthread = SearchThread(subtext)
            self.searchthread.finishSignal.connect(self.refreshUI)
            self.searchthread.start()

    def refreshUI(self):
        self.tableWidget.clearContents()
        self.retranslateUi(Form)
        self.subplupbt.setDisabled(False)
        self.refreshpbt.setDisabled(False)

    # table内添加数据
    def adddata(self):

        content  = readFile()
        with open("subscribe.json", "r") as dump_f:
            temp = load(dump_f)
            temp_num = temp['total']
            temp_con = temp['list']

        for row_number in range(temp_num):
            self.tableWidget.insertRow(row_number)
            self.tableWidget.setItem(row_number, 0, QtGui.QTableWidgetItem((temp_con[row_number]['name'])))
            self.tableWidget.setItem(row_number, 1, QtGui.QTableWidgetItem(str(temp_con[row_number]['lastEpisode'])))
            self.tableWidget.setItem(row_number, 2, QtGui.QTableWidgetItem((temp_con[row_number]['sourceName'])))

            strrr = '''<a style= "color:#55aaff; text-decoration:none; font-size:11pt; font-family:Consolas; font-weight: bold;" \ 
            href="''' + temp_con[row_number]['address'] + '''">(Open Url)</a>'''

            version = QLabel(strrr, self)
            version.setOpenExternalLinks(True)
            self.tableWidget.setCellWidget(row_number, 3, version)
            self.tableWidget.setCellWidget(row_number, 4, self.buttonForRow(row_number))

    def buttonForRow(self,id):
        widget=QWidget()
        # 修改
        deleteBtn = QPushButton(_fromUtf8('移出订阅'))
        deleteBtn.setFont(QtGui.QFont("Microsoft YaHei", 11))
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
        deleateSubscribeList(id)
        self.tableWidget.clearContents()
        self.retranslateUi(Form)

class warningBox(QDialog):
    def __init__(self,str_title,str_text,list_bool):#####自己写一个warningbox
        super(warningBox,self).__init__(parent = None)
        self.return_value = list_bool
        self.setWindowTitle(str_title)
        self.mainlayout = QGridLayout(self)
        self.labelText = QLabel()
        self.setFont(QtGui.QFont("Microsoft YaHei", 11))#####字体设置
        self.mainlayout.addWidget(self.labelText,0,0,1,10)
        self.labelText.setText(str_text)
        self.resize(400,100)
        self.buttonSure = QPushButton()
        self.buttonSure.setText(u"确定" )
        self.buttonCancel = QPushButton()
        self.buttonCancel.setText(u"取消" )
        self.mainlayout.addWidget(self.buttonSure,1,2,1,2)
        self.mainlayout.addWidget(self.buttonCancel,1,6,1,2)
        self.setLayout(self.mainlayout)
        self.buttonSure.clicked.connect(self.sureOpra)
        self.buttonCancel.clicked.connect(self.cancelOpra)
        self.show()

    def sureOpra(self):
        self.close()
        self.return_value.append(1)

    def cancelOpra(self):
        self.close()
        self.return_value.append(0)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
