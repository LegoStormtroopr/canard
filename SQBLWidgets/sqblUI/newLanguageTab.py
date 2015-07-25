# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/newLanguageTab.ui'
#
# Created: Sat Jul 25 11:37:42 2015
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
        Form.resize(543, 475)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 75, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 322, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        self.languageList = QtGui.QComboBox(Form)
        self.languageList.setObjectName(_fromUtf8("languageList"))
        self.gridLayout.addWidget(self.languageList, 2, 0, 1, 1)
        self.addLanguage = QtGui.QPushButton(Form)
        self.addLanguage.setMaximumSize(QtCore.QSize(100, 16777215))
        self.addLanguage.setObjectName(_fromUtf8("addLanguage"))
        self.gridLayout.addWidget(self.addLanguage, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "To add some textual information select a new language for the text from the list below:", None, QtGui.QApplication.UnicodeUTF8))
        self.addLanguage.setText(QtGui.QApplication.translate("Form", "Add", None, QtGui.QApplication.UnicodeUTF8))

