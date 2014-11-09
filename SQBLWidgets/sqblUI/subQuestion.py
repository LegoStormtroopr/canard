# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/subQuestion.ui'
#
# Created: Sat Jun 14 16:40:06 2014
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
        Form.resize(519, 396)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.languages = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.languages.sizePolicy().hasHeightForWidth())
        self.languages.setSizePolicy(sizePolicy)
        self.languages.setEditable(False)
        self.languages.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.languages.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.languages.setObjectName(_fromUtf8("languages"))
        self.horizontalLayout.addWidget(self.languages)
        self.removeLanguage = QtGui.QPushButton(Form)
        self.removeLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.removeLanguage.setObjectName(_fromUtf8("removeLanguage"))
        self.horizontalLayout.addWidget(self.removeLanguage)
        self.addLanguage = QtGui.QPushButton(Form)
        self.addLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.addLanguage.setObjectName(_fromUtf8("addLanguage"))
        self.horizontalLayout.addWidget(self.addLanguage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        self.subQuestionList = QtGui.QTableWidget(Form)
        self.subQuestionList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.subQuestionList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.subQuestionList.setColumnCount(1)
        self.subQuestionList.setObjectName(_fromUtf8("subQuestionList"))
        self.subQuestionList.setRowCount(0)
        self.subQuestionList.horizontalHeader().setVisible(False)
        self.subQuestionList.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.subQuestionList)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.addSubQuestionBtn = QtGui.QPushButton(Form)
        self.addSubQuestionBtn.setObjectName(_fromUtf8("addSubQuestionBtn"))
        self.horizontalLayout_2.addWidget(self.addSubQuestionBtn)
        self.removeSubQuestionBtn = QtGui.QPushButton(Form)
        self.removeSubQuestionBtn.setObjectName(_fromUtf8("removeSubQuestionBtn"))
        self.horizontalLayout_2.addWidget(self.removeSubQuestionBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.removeLanguage.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.addLanguage.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "All subquestions below will be required to answer for all responses for this question.", None, QtGui.QApplication.UnicodeUTF8))
        self.addSubQuestionBtn.setText(QtGui.QApplication.translate("Form", " Add SubQuestion ", None, QtGui.QApplication.UnicodeUTF8))
        self.removeSubQuestionBtn.setText(QtGui.QApplication.translate("Form", " Remove SubQuestion ", None, QtGui.QApplication.UnicodeUTF8))

