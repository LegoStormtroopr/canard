# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/bulkQuestionEditor.ui'
#
# Created: Sun Nov 30 11:26:55 2014
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
        Form.resize(538, 528)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.languages = QtGui.QComboBox(Form)
        self.languages.setObjectName(_fromUtf8("languages"))
        self.horizontalLayout.addWidget(self.languages)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.questionList = ReturnSupportedTableWidget(Form)
        self.questionList.setObjectName(_fromUtf8("questionList"))
        self.questionList.setColumnCount(3)
        self.questionList.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.questionList.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.questionList.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.questionList.setHorizontalHeaderItem(2, item)
        self.questionList.horizontalHeader().setStretchLastSection(True)
        self.questionList.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.questionList)
        self.actionAddQuestion = QtGui.QAction(Form)
        self.actionAddQuestion.setObjectName(_fromUtf8("actionAddQuestion"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.questionList.setSortingEnabled(True)
        item = self.questionList.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Form", "Name", None, QtGui.QApplication.UnicodeUTF8))
        item = self.questionList.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Form", "Response Type", None, QtGui.QApplication.UnicodeUTF8))
        item = self.questionList.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("Form", "Question Text", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddQuestion.setText(QtGui.QApplication.translate("Form", "Add Question", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddQuestion.setShortcut(QtGui.QApplication.translate("Form", "Ctrl+A, Ctrl+Shift+J", None, QtGui.QApplication.UnicodeUTF8))

from canardCustomQtWidgets import ReturnSupportedTableWidget
