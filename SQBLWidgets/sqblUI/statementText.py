# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/statementText.ui'
#
# Created: Sat Jul 25 12:17:11 2015
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
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.statementText = QtGui.QTextEdit(Form)
        self.statementText.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.statementText.setObjectName(_fromUtf8("statementText"))
        self.verticalLayout.addWidget(self.statementText)
        self.label.setBuddy(self.statementText)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Statement Text</span> - <small>The text shown to a respondent.</small></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

