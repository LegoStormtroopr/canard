# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/responseCodeList.ui'
#
# Created: Sat Jul 25 12:16:52 2015
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
        Form.resize(488, 448)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
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
        self.languages.setEditable(False)
        self.languages.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.languages.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.languages.setObjectName(_fromUtf8("languages"))
        self.horizontalLayout.addWidget(self.languages)
        self.addLanguage = QtGui.QPushButton(Form)
        self.addLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.addLanguage.setObjectName(_fromUtf8("addLanguage"))
        self.horizontalLayout.addWidget(self.addLanguage)
        self.removeLanguage = QtGui.QPushButton(Form)
        self.removeLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.removeLanguage.setObjectName(_fromUtf8("removeLanguage"))
        self.horizontalLayout.addWidget(self.removeLanguage)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 4)
        self.hasMinSelections = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hasMinSelections.sizePolicy().hasHeightForWidth())
        self.hasMinSelections.setSizePolicy(sizePolicy)
        self.hasMinSelections.setObjectName(_fromUtf8("hasMinSelections"))
        self.gridLayout.addWidget(self.hasMinSelections, 1, 0, 1, 1)
        self.minSelections = QtGui.QSpinBox(Form)
        self.minSelections.setEnabled(False)
        self.minSelections.setMinimum(1)
        self.minSelections.setMaximum(1000)
        self.minSelections.setProperty("value", 1)
        self.minSelections.setObjectName(_fromUtf8("minSelections"))
        self.gridLayout.addWidget(self.minSelections, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.minSelectionsHint = QtGui.QLineEdit(Form)
        self.minSelectionsHint.setEnabled(False)
        self.minSelectionsHint.setObjectName(_fromUtf8("minSelectionsHint"))
        self.gridLayout.addWidget(self.minSelectionsHint, 2, 1, 1, 3)
        self.hasMaxSelections = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hasMaxSelections.sizePolicy().hasHeightForWidth())
        self.hasMaxSelections.setSizePolicy(sizePolicy)
        self.hasMaxSelections.setObjectName(_fromUtf8("hasMaxSelections"))
        self.gridLayout.addWidget(self.hasMaxSelections, 3, 0, 1, 1)
        self.maxSelections = QtGui.QSpinBox(Form)
        self.maxSelections.setEnabled(False)
        self.maxSelections.setMinimum(1)
        self.maxSelections.setMaximum(1000)
        self.maxSelections.setProperty("value", 1)
        self.maxSelections.setObjectName(_fromUtf8("maxSelections"))
        self.gridLayout.addWidget(self.maxSelections, 3, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.maxSelectionsHint = QtGui.QLineEdit(Form)
        self.maxSelectionsHint.setEnabled(False)
        self.maxSelectionsHint.setObjectName(_fromUtf8("maxSelectionsHint"))
        self.gridLayout.addWidget(self.maxSelectionsHint, 4, 1, 1, 3)
        self.codeListTable = QtGui.QTableWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.codeListTable.sizePolicy().hasHeightForWidth())
        self.codeListTable.setSizePolicy(sizePolicy)
        self.codeListTable.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.codeListTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.codeListTable.setObjectName(_fromUtf8("codeListTable"))
        self.codeListTable.setColumnCount(3)
        self.codeListTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.codeListTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.codeListTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.codeListTable.setHorizontalHeaderItem(2, item)
        self.codeListTable.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.codeListTable, 5, 0, 1, 4)
        self.addCode = QtGui.QPushButton(Form)
        self.addCode.setObjectName(_fromUtf8("addCode"))
        self.gridLayout.addWidget(self.addCode, 6, 2, 1, 1)
        self.removeCode = QtGui.QPushButton(Form)
        self.removeCode.setObjectName(_fromUtf8("removeCode"))
        self.gridLayout.addWidget(self.removeCode, 6, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.hasMinSelections, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.minSelectionsHint.setEnabled)
        QtCore.QObject.connect(self.hasMaxSelections, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.maxSelectionsHint.setEnabled)
        QtCore.QObject.connect(self.hasMinSelections, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.minSelections.setEnabled)
        QtCore.QObject.connect(self.hasMaxSelections, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.maxSelections.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Language", None, QtGui.QApplication.UnicodeUTF8))
        self.addLanguage.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.removeLanguage.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.hasMinSelections.setText(QtGui.QApplication.translate("Form", "Minimum Selections", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Hint", None, QtGui.QApplication.UnicodeUTF8))
        self.hasMaxSelections.setText(QtGui.QApplication.translate("Form", "Maximum Selections", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Hint", None, QtGui.QApplication.UnicodeUTF8))
        item = self.codeListTable.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Form", "Code", None, QtGui.QApplication.UnicodeUTF8))
        item = self.codeListTable.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Form", "Free text", None, QtGui.QApplication.UnicodeUTF8))
        item = self.codeListTable.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("Form", "Text", None, QtGui.QApplication.UnicodeUTF8))
        self.addCode.setText(QtGui.QApplication.translate("Form", "Add code", None, QtGui.QApplication.UnicodeUTF8))
        self.removeCode.setText(QtGui.QApplication.translate("Form", "Remove Code", None, QtGui.QApplication.UnicodeUTF8))

