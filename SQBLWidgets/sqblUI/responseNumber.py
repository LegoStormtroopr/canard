# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/responseNumber.ui'
#
# Created: Sun Nov 30 11:27:08 2014
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
        Form.resize(505, 356)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hasSuffix = QtGui.QCheckBox(Form)
        self.hasSuffix.setObjectName(_fromUtf8("hasSuffix"))
        self.gridLayout.addWidget(self.hasSuffix, 3, 0, 1, 1)
        self.removeLanguage = QtGui.QPushButton(Form)
        self.removeLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.removeLanguage.setObjectName(_fromUtf8("removeLanguage"))
        self.gridLayout.addWidget(self.removeLanguage, 0, 3, 1, 1)
        self.displayHint = QtGui.QLineEdit(Form)
        self.displayHint.setEnabled(False)
        self.displayHint.setText(_fromUtf8(""))
        self.displayHint.setObjectName(_fromUtf8("displayHint"))
        self.gridLayout.addWidget(self.displayHint, 1, 1, 1, 3)
        self.line_3 = QtGui.QFrame(Form)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 7, 1, 1, 3)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 9, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 12, 0, 1, 1)
        self.hasMinValue = QtGui.QCheckBox(Form)
        self.hasMinValue.setObjectName(_fromUtf8("hasMinValue"))
        self.gridLayout.addWidget(self.hasMinValue, 5, 0, 1, 1)
        self.hasStepValue = QtGui.QCheckBox(Form)
        self.hasStepValue.setObjectName(_fromUtf8("hasStepValue"))
        self.gridLayout.addWidget(self.hasStepValue, 11, 0, 1, 1)
        self.stepValueHint = QtGui.QLineEdit(Form)
        self.stepValueHint.setEnabled(False)
        self.stepValueHint.setObjectName(_fromUtf8("stepValueHint"))
        self.gridLayout.addWidget(self.stepValueHint, 12, 1, 1, 3)
        self.hasMaxValue = QtGui.QCheckBox(Form)
        self.hasMaxValue.setObjectName(_fromUtf8("hasMaxValue"))
        self.gridLayout.addWidget(self.hasMaxValue, 8, 0, 1, 1)
        self.prefix = QtGui.QLineEdit(Form)
        self.prefix.setEnabled(False)
        self.prefix.setObjectName(_fromUtf8("prefix"))
        self.gridLayout.addWidget(self.prefix, 2, 1, 1, 3)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.minValueHint = QtGui.QLineEdit(Form)
        self.minValueHint.setEnabled(False)
        self.minValueHint.setObjectName(_fromUtf8("minValueHint"))
        self.gridLayout.addWidget(self.minValueHint, 6, 1, 1, 3)
        self.stepValue = QtGui.QDoubleSpinBox(Form)
        self.stepValue.setEnabled(False)
        self.stepValue.setMaximumSize(QtCore.QSize(16777211, 16777215))
        self.stepValue.setSpecialValueText(_fromUtf8(""))
        self.stepValue.setPrefix(_fromUtf8(""))
        self.stepValue.setSuffix(_fromUtf8(""))
        self.stepValue.setDecimals(5)
        self.stepValue.setMinimum(-16777214.0)
        self.stepValue.setMaximum(16777214.0)
        self.stepValue.setProperty("value", 1.0)
        self.stepValue.setObjectName(_fromUtf8("stepValue"))
        self.gridLayout.addWidget(self.stepValue, 11, 1, 1, 3)
        self.maxValueHint = QtGui.QLineEdit(Form)
        self.maxValueHint.setEnabled(False)
        self.maxValueHint.setObjectName(_fromUtf8("maxValueHint"))
        self.gridLayout.addWidget(self.maxValueHint, 9, 1, 1, 3)
        self.line_2 = QtGui.QFrame(Form)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 10, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 13, 1, 1, 1)
        self.minValue = QtGui.QDoubleSpinBox(Form)
        self.minValue.setEnabled(False)
        self.minValue.setPrefix(_fromUtf8(""))
        self.minValue.setSuffix(_fromUtf8(""))
        self.minValue.setDecimals(5)
        self.minValue.setMinimum(-16777214.0)
        self.minValue.setMaximum(16777214.0)
        self.minValue.setObjectName(_fromUtf8("minValue"))
        self.gridLayout.addWidget(self.minValue, 5, 1, 1, 3)
        self.maxValue = QtGui.QDoubleSpinBox(Form)
        self.maxValue.setEnabled(False)
        self.maxValue.setDecimals(5)
        self.maxValue.setMinimum(-16777214.0)
        self.maxValue.setMaximum(16777214.0)
        self.maxValue.setObjectName(_fromUtf8("maxValue"))
        self.gridLayout.addWidget(self.maxValue, 8, 1, 1, 3)
        self.suffix = QtGui.QLineEdit(Form)
        self.suffix.setEnabled(False)
        self.suffix.setObjectName(_fromUtf8("suffix"))
        self.gridLayout.addWidget(self.suffix, 3, 1, 1, 1)
        self.hasPrefix = QtGui.QCheckBox(Form)
        self.hasPrefix.setObjectName(_fromUtf8("hasPrefix"))
        self.gridLayout.addWidget(self.hasPrefix, 2, 0, 1, 1)
        self.hasDisplayHint = QtGui.QCheckBox(Form)
        self.hasDisplayHint.setObjectName(_fromUtf8("hasDisplayHint"))
        self.gridLayout.addWidget(self.hasDisplayHint, 1, 0, 1, 1)
        self.addLanguage = QtGui.QPushButton(Form)
        self.addLanguage.setMaximumSize(QtCore.QSize(30, 16777215))
        self.addLanguage.setObjectName(_fromUtf8("addLanguage"))
        self.gridLayout.addWidget(self.addLanguage, 0, 2, 1, 1)
        self.languages = QtGui.QComboBox(Form)
        self.languages.setEditable(False)
        self.languages.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.languages.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.languages.setObjectName(_fromUtf8("languages"))
        self.gridLayout.addWidget(self.languages, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.hasMinValue, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.minValueHint.setEnabled)
        QtCore.QObject.connect(self.hasMaxValue, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.maxValueHint.setEnabled)
        QtCore.QObject.connect(self.hasStepValue, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.stepValue.setEnabled)
        QtCore.QObject.connect(self.hasStepValue, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.stepValueHint.setEnabled)
        QtCore.QObject.connect(self.hasMinValue, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.minValue.setEnabled)
        QtCore.QObject.connect(self.hasMaxValue, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.maxValue.setEnabled)
        QtCore.QObject.connect(self.hasDisplayHint, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.displayHint.setEnabled)
        QtCore.QObject.connect(self.hasPrefix, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.prefix.setEnabled)
        QtCore.QObject.connect(self.hasSuffix, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.suffix.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.languages, self.displayHint)
        Form.setTabOrder(self.displayHint, self.prefix)
        Form.setTabOrder(self.prefix, self.minValue)
        Form.setTabOrder(self.minValue, self.minValueHint)
        Form.setTabOrder(self.minValueHint, self.maxValue)
        Form.setTabOrder(self.maxValue, self.maxValueHint)
        Form.setTabOrder(self.maxValueHint, self.stepValue)
        Form.setTabOrder(self.stepValue, self.stepValueHint)
        Form.setTabOrder(self.stepValueHint, self.hasStepValue)
        Form.setTabOrder(self.hasStepValue, self.hasMinValue)
        Form.setTabOrder(self.hasMinValue, self.hasMaxValue)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.hasSuffix.setText(QtGui.QApplication.translate("Form", "Suffix", None, QtGui.QApplication.UnicodeUTF8))
        self.removeLanguage.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.displayHint.setPlaceholderText(QtGui.QApplication.translate("Form", "Optionally shown to assist with the response (like a placeholder like this)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Hint", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Hint", None, QtGui.QApplication.UnicodeUTF8))
        self.hasMinValue.setText(QtGui.QApplication.translate("Form", "Minimum Value", None, QtGui.QApplication.UnicodeUTF8))
        self.hasStepValue.setText(QtGui.QApplication.translate("Form", "Multiples of", None, QtGui.QApplication.UnicodeUTF8))
        self.hasMaxValue.setText(QtGui.QApplication.translate("Form", "Maximum Value", None, QtGui.QApplication.UnicodeUTF8))
        self.prefix.setPlaceholderText(QtGui.QApplication.translate("Form", "e.g. $, €, £", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Hint", None, QtGui.QApplication.UnicodeUTF8))
        self.suffix.setPlaceholderText(QtGui.QApplication.translate("Form", "e.g. \"per acre\", \",000\", etc...", None, QtGui.QApplication.UnicodeUTF8))
        self.hasPrefix.setText(QtGui.QApplication.translate("Form", "Prefix", None, QtGui.QApplication.UnicodeUTF8))
        self.hasDisplayHint.setText(QtGui.QApplication.translate("Form", "Display Hint", None, QtGui.QApplication.UnicodeUTF8))
        self.addLanguage.setText(QtGui.QApplication.translate("Form", "+", None, QtGui.QApplication.UnicodeUTF8))

