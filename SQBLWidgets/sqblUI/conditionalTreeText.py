# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/conditionalTreeText.ui'
#
# Created: Sat Jul 25 12:16:40 2015
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
        Form.resize(534, 454)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setStyleSheet(_fromUtf8("margin-top:8px;"))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.purpose = QtGui.QTextEdit(Form)
        self.purpose.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.purpose.setAcceptRichText(False)
        self.purpose.setObjectName(_fromUtf8("purpose"))
        self.verticalLayout.addWidget(self.purpose)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setStyleSheet(_fromUtf8("margin-top:8px;"))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.instruction = QtGui.QTextEdit(Form)
        self.instruction.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.instruction.setObjectName(_fromUtf8("instruction"))
        self.verticalLayout.addWidget(self.instruction)
        self.label_2.setBuddy(self.purpose)
        self.label_5.setBuddy(self.instruction)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Purpose</span> - <span style=\" font-size:small;\">Why are respondents going to be routed according to this object</span>:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Instruction</span> - <small>Extra text about this routing and sequencing that may be shown to a respondent depending on the final questionnaire</small>:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

