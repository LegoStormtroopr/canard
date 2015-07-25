# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/responseBoolean.ui'
#
# Created: Sat Jul 25 11:37:43 2015
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
        Form.resize(378, 220)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.displayHint = QtGui.QLineEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayHint.sizePolicy().hasHeightForWidth())
        self.displayHint.setSizePolicy(sizePolicy)
        self.displayHint.setObjectName(_fromUtf8("displayHint"))
        self.gridLayout.addWidget(self.displayHint, 1, 1, 1, 2)
        self.hasDisplayHint = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hasDisplayHint.sizePolicy().hasHeightForWidth())
        self.hasDisplayHint.setSizePolicy(sizePolicy)
        self.hasDisplayHint.setMinimumSize(QtCore.QSize(90, 0))
        self.hasDisplayHint.setMaximumSize(QtCore.QSize(110, 16777215))
        self.hasDisplayHint.setObjectName(_fromUtf8("hasDisplayHint"))
        self.gridLayout.addWidget(self.hasDisplayHint, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.languages = QtGui.QComboBox(Form)
        self.languages.setEditable(False)
        self.languages.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.languages.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.languages.setObjectName(_fromUtf8("languages"))
        self.horizontalLayout_3.addWidget(self.languages)
        self.addLanguage = QtGui.QPushButton(Form)
        self.addLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.addLanguage.setObjectName(_fromUtf8("addLanguage"))
        self.horizontalLayout_3.addWidget(self.addLanguage)
        self.removeLanguage = QtGui.QPushButton(Form)
        self.removeLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.removeLanguage.setObjectName(_fromUtf8("removeLanguage"))
        self.horizontalLayout_3.addWidget(self.removeLanguage)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.displayHint.setPlaceholderText(QtGui.QApplication.translate("Form", "Optionally shown to assist with the response (like a placeholder like this)", None, QtGui.QApplication.UnicodeUTF8))
        self.hasDisplayHint.setText(QtGui.QApplication.translate("Form", "Display Hint", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.addLanguage.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.removeLanguage.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))

