# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/wordSub.ui'
#
# Created: Sat Jul 25 12:17:17 2015
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
        Form.resize(479, 372)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
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
        self.horizontalLayout_2.addWidget(self.label_5)
        self.name = QtGui.QLineEdit(Form)
        self.name.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setPlaceholderText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.horizontalLayout_2.addWidget(self.name)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.textTab = QtGui.QWidget(Form)
        self.textTab.setObjectName(_fromUtf8("textTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.textTab)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2.addWidget(self.textTab)
        self.label = QtGui.QLabel(Form)
        self.label.setStyleSheet(_fromUtf8("* {font-size:8pt; }"))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.DTLayout = QtGui.QHBoxLayout()
        self.DTLayout.setObjectName(_fromUtf8("DTLayout"))
        self.verticalLayout_2.addLayout(self.DTLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addCondition = QtGui.QPushButton(Form)
        self.addCondition.setObjectName(_fromUtf8("addCondition"))
        self.horizontalLayout.addWidget(self.addCondition)
        self.removeCondition = QtGui.QPushButton(Form)
        self.removeCondition.setObjectName(_fromUtf8("removeCondition"))
        self.horizontalLayout.addWidget(self.removeCondition)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.label_5.setBuddy(self.name)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setToolTip(QtGui.QApplication.translate("Form", "Shown at the initialisation of a form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Wordsub Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p>Drag questions from the components tree to the top header to add new columns.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.addCondition.setText(QtGui.QApplication.translate("Form", "Add Condition", None, QtGui.QApplication.UnicodeUTF8))
        self.removeCondition.setText(QtGui.QApplication.translate("Form", "Remove Condition", None, QtGui.QApplication.UnicodeUTF8))

