# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/languagePicker.ui'
#
# Created: Sat Jul 25 11:37:34 2015
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
        Form.resize(546, 41)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.removeLanguageButton = QtGui.QPushButton(Form)
        self.removeLanguageButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.removeLanguageButton.setObjectName(_fromUtf8("removeLanguageButton"))
        self.gridLayout.addWidget(self.removeLanguageButton, 0, 3, 1, 1)
        self.addLanguageButton = QtGui.QPushButton(Form)
        self.addLanguageButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.addLanguageButton.setObjectName(_fromUtf8("addLanguageButton"))
        self.gridLayout.addWidget(self.addLanguageButton, 0, 2, 1, 1)
        self.languageList = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.languageList.sizePolicy().hasHeightForWidth())
        self.languageList.setSizePolicy(sizePolicy)
        self.languageList.setEditable(False)
        self.languageList.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.languageList.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.languageList.setObjectName(_fromUtf8("languageList"))
        self.gridLayout.addWidget(self.languageList, 0, 1, 1, 1)
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.removeLanguageButton.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.addLanguageButton.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Language:", None, QtGui.QApplication.UnicodeUTF8))

