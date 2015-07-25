# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/questionText.ui'
#
# Created: Sat Jul 25 11:38:00 2015
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
        Form.resize(546, 253)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.questionText = QtGui.QTextEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.questionText.sizePolicy().hasHeightForWidth())
        self.questionText.setSizePolicy(sizePolicy)
        self.questionText.setMinimumSize(QtCore.QSize(0, 50))
        self.questionText.setBaseSize(QtCore.QSize(0, 0))
        self.questionText.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.questionText.setObjectName(_fromUtf8("questionText"))
        self.verticalLayout.addWidget(self.questionText)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setStyleSheet(_fromUtf8("margin-top:8px;"))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.questionIntent = QtGui.QTextEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.questionIntent.sizePolicy().hasHeightForWidth())
        self.questionIntent.setSizePolicy(sizePolicy)
        self.questionIntent.setMinimumSize(QtCore.QSize(0, 50))
        self.questionIntent.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.questionIntent.setAcceptRichText(False)
        self.questionIntent.setObjectName(_fromUtf8("questionIntent"))
        self.verticalLayout.addWidget(self.questionIntent)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setStyleSheet(_fromUtf8("margin-top:8px;"))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.instruction = QtGui.QTextEdit(Form)
        self.instruction.setMinimumSize(QtCore.QSize(0, 50))
        self.instruction.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.instruction.setObjectName(_fromUtf8("instruction"))
        self.verticalLayout.addWidget(self.instruction)
        self.label.setBuddy(self.questionText)
        self.label_2.setBuddy(self.questionIntent)
        self.label_5.setBuddy(self.instruction)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Question Text</span> - <small>The text shown to a respondent to attempt to collect the data required by the data element.</small></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Question Intent</span> - <small>A brief description of why this question is being asked in this way.</small></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Instruction</span> - <small>Extra text that adds context to a question shown near a question or read to a respondent depending on the final questionnaire.</small></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

