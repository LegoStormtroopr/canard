# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wordSubText.ui'
#
# Created: Sat Jul 25 11:38:16 2015
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
        Form.resize(400, 90)
        self.formLayout = QtGui.QFormLayout(Form)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_5 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(90, 0))
        self.label_5.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.intentText = QtGui.QLineEdit(Form)
        self.intentText.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intentText.sizePolicy().hasHeightForWidth())
        self.intentText.setSizePolicy(sizePolicy)
        self.intentText.setObjectName(_fromUtf8("intentText"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.intentText)
        self.label_3 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(90, 0))
        self.label_3.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.defaultText = QtGui.QLineEdit(Form)
        self.defaultText.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.defaultText.sizePolicy().hasHeightForWidth())
        self.defaultText.setSizePolicy(sizePolicy)
        self.defaultText.setObjectName(_fromUtf8("defaultText"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.defaultText)
        self.label_4 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(90, 0))
        self.label_4.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.staticText = QtGui.QLineEdit(Form)
        self.staticText.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staticText.sizePolicy().hasHeightForWidth())
        self.staticText.setSizePolicy(sizePolicy)
        self.staticText.setObjectName(_fromUtf8("staticText"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.staticText)
        self.label_5.setBuddy(self.intentText)
        self.label_3.setBuddy(self.defaultText)
        self.label_4.setBuddy(self.staticText)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.intentText, self.defaultText)
        Form.setTabOrder(self.defaultText, self.staticText)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setToolTip(QtGui.QApplication.translate("Form", "Shown at the initialisation of a form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Intent:", None, QtGui.QApplication.UnicodeUTF8))
        self.intentText.setPlaceholderText(QtGui.QApplication.translate("Form", "What is the purpose of the word sub", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setToolTip(QtGui.QApplication.translate("Form", "Shown at the initialisation of a form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Default:", None, QtGui.QApplication.UnicodeUTF8))
        self.defaultText.setPlaceholderText(QtGui.QApplication.translate("Form", "Shown at the initialisation of a form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Static:", None, QtGui.QApplication.UnicodeUTF8))
        self.staticText.setPlaceholderText(QtGui.QApplication.translate("Form", "Shown if dynamic functionality is not enabled", None, QtGui.QApplication.UnicodeUTF8))

