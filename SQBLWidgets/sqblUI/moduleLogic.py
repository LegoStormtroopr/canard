# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/moduleLogic.ui'
#
# Created: Sat Jun 14 16:40:02 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabBulkQuestionEditor = QtGui.QWidget()
        self.tabBulkQuestionEditor.setToolTip(_fromUtf8(""))
        self.tabBulkQuestionEditor.setObjectName(_fromUtf8("tabBulkQuestionEditor"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabBulkQuestionEditor)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget.addTab(self.tabBulkQuestionEditor, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabBulkQuestionEditor), QtGui.QApplication.translate("Form", "Bulk Question Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tabBulkQuestionEditor), QtGui.QApplication.translate("Form", "Use the bulk editor to quickly add and change questions.\n"
"Press enter to move between fields, when pressing enter on the last field a new question is added to the end of the main sequence.", None, QtGui.QApplication.UnicodeUTF8))

