# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/questionModuleText.ui'
#
# Created: Sun Nov 30 11:27:14 2014
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
        Form.resize(580, 458)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.longName = QtGui.QLineEdit(Form)
        self.longName.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.longName.setObjectName(_fromUtf8("longName"))
        self.verticalLayout.addWidget(self.longName)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.title = QtGui.QLineEdit(Form)
        self.title.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.title.setObjectName(_fromUtf8("title"))
        self.verticalLayout.addWidget(self.title)
        self.label = QtGui.QLabel(Form)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.targetRespondent = QtGui.QTextEdit(Form)
        self.targetRespondent.setMaximumSize(QtCore.QSize(16777215, 50))
        self.targetRespondent.setStyleSheet(_fromUtf8("margin-left:8px;"))
        self.targetRespondent.setAcceptRichText(False)
        self.targetRespondent.setObjectName(_fromUtf8("targetRespondent"))
        self.verticalLayout.addWidget(self.targetRespondent)
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
        self.label_2.setBuddy(self.purpose)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Long Name</span> - <span style=\" font-size:small;\">This will be shown to survey designers when searching for modules.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Title</span> - <span style=\" font-size:small;\">The name of this module as presented to a respondent of a survey.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Target Respondent</span> - <span style=\" font-size:small;\">The people who this module is specifically trying to gather data from.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Purpose</span> - <span style=\" font-size:small;\">Why do respondents need to complete this module.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

