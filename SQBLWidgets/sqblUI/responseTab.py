# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/responseTab.ui'
#
# Created: Sat Jul 25 12:17:00 2015
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
        Form.resize(699, 489)
        self.scrollArea = QtGui.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 657, 444))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 655, 442))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_7 = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.line = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_8.setStyleSheet(_fromUtf8(""))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 4, 0, 3, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 6, 1, 1, 1)
        self.responsePlaceHolder = QtGui.QVBoxLayout()
        self.responsePlaceHolder.setObjectName(_fromUtf8("responsePlaceHolder"))
        self.gridLayout_2.addLayout(self.responsePlaceHolder, 4, 1, 2, 1)
        self.widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.canDontKnow = QtGui.QRadioButton(self.widget)
        self.canDontKnow.setObjectName(_fromUtf8("canDontKnow"))
        self.verticalLayout_3.addWidget(self.canDontKnow)
        self.radioButton_3 = QtGui.QRadioButton(self.widget)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.verticalLayout_3.addWidget(self.radioButton_3)
        self.gridLayout_2.addWidget(self.widget, 2, 1, 1, 1)
        self.widget_2 = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.canRefuse = QtGui.QRadioButton(self.widget_2)
        self.canRefuse.setObjectName(_fromUtf8("canRefuse"))
        self.verticalLayout_4.addWidget(self.canRefuse)
        self.radioButton = QtGui.QRadioButton(self.widget_2)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.verticalLayout_4.addWidget(self.radioButton)
        self.gridLayout_2.addWidget(self.widget_2, 0, 1, 1, 1)
        self.responseType = QtGui.QComboBox(self.scrollAreaWidgetContents)
        self.responseType.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.responseType.setObjectName(_fromUtf8("responseType"))
        self.gridLayout_2.addWidget(self.responseType, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Don\'t know", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Refusal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "\n"
"Language", None, QtGui.QApplication.UnicodeUTF8))
        self.canDontKnow.setText(QtGui.QApplication.translate("Form", "Allowed", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_3.setText(QtGui.QApplication.translate("Form", "Not Allowed", None, QtGui.QApplication.UnicodeUTF8))
        self.canRefuse.setText(QtGui.QApplication.translate("Form", "Can Refuse", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("Form", "Must answer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Response Type", None, QtGui.QApplication.UnicodeUTF8))

