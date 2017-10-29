#!/usr/bin/env python
# coding=utf-8
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
import sys
from mainui import Ui_Form

class mywindow(QWidget, Ui_Form):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)







    def subfunc(self):
        a=1

    def refreshfunc(self):
        a=1




app = QApplication(sys.argv)
window = mywindow()
window.show()
sys.exit(app.exec_())