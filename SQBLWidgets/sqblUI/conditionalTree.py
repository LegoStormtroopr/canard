# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/conditionalTree.ui'
#
# Created: Sat Jul 25 11:37:30 2015
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
        Form.resize(566, 352)
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.name = QtGui.QLineEdit(Form)
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.gridLayout_3.addWidget(self.name, 0, 1, 1, 2)
        self.conditionalTreeTabs = QtGui.QTabWidget(Form)
        self.conditionalTreeTabs.setObjectName(_fromUtf8("conditionalTreeTabs"))
        self.textTab = QtGui.QWidget()
        self.textTab.setObjectName(_fromUtf8("textTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.textTab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.conditionalTreeTabs.addTab(self.textTab, _fromUtf8(""))
        self.tabWidgetPage1 = QtGui.QWidget()
        self.tabWidgetPage1.setObjectName(_fromUtf8("tabWidgetPage1"))
        self.gridLayout = QtGui.QGridLayout(self.tabWidgetPage1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.deleteBranch = QtGui.QPushButton(self.tabWidgetPage1)
        self.deleteBranch.setObjectName(_fromUtf8("deleteBranch"))
        self.gridLayout.addWidget(self.deleteBranch, 1, 2, 1, 1)
        self.addBranch = QtGui.QPushButton(self.tabWidgetPage1)
        self.addBranch.setObjectName(_fromUtf8("addBranch"))
        self.gridLayout.addWidget(self.addBranch, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.branchList = QtGui.QListWidget(self.tabWidgetPage1)
        self.branchList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.branchList.setObjectName(_fromUtf8("branchList"))
        self.gridLayout.addWidget(self.branchList, 2, 0, 1, 3)
        self.label_2 = QtGui.QLabel(self.tabWidgetPage1)
        self.label_2.setStyleSheet(_fromUtf8("font-size:8pt;"))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 3)
        self.conditionalTreeTabs.addTab(self.tabWidgetPage1, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.line = QtGui.QFrame(self.tab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 2, 0, 1, 2)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setToolTip(_fromUtf8(""))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)
        self.defaultBranch = QtGui.QComboBox(self.tab)
        self.defaultBranch.setMinimumSize(QtCore.QSize(150, 0))
        self.defaultBranch.setMaximumSize(QtCore.QSize(250, 16777215))
        self.defaultBranch.setObjectName(_fromUtf8("defaultBranch"))
        self.gridLayout_2.addWidget(self.defaultBranch, 4, 1, 1, 1)
        self.DTLayout = QtGui.QHBoxLayout()
        self.DTLayout.setObjectName(_fromUtf8("DTLayout"))
        self.gridLayout_2.addLayout(self.DTLayout, 1, 0, 1, 2)
        self.label = QtGui.QLabel(self.tab)
        self.label.setStyleSheet(_fromUtf8("* {font-size:8pt; }"))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 3, 2)
        self.conditionalTreeTabs.addTab(self.tab, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.conditionalTreeTabs, 1, 0, 1, 3)
        self.label_4.setBuddy(self.name)

        self.retranslateUi(Form)
        self.conditionalTreeTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Conditional Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.conditionalTreeTabs.setTabText(self.conditionalTreeTabs.indexOf(self.textTab), QtGui.QApplication.translate("Form", "Text", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteBranch.setText(QtGui.QApplication.translate("Form", "Delete Branch", None, QtGui.QApplication.UnicodeUTF8))
        self.addBranch.setText(QtGui.QApplication.translate("Form", "Add Branch", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p>Respondents will be sequenced into <span style=\" text-decoration: underline;\">only one</span> of the branches below based the sequence guide.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.conditionalTreeTabs.setTabText(self.conditionalTreeTabs.indexOf(self.tabWidgetPage1), QtGui.QApplication.translate("Form", "Branches", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Default Branch: </span><span style=\" font-size:8pt;\">An optional branch that will be performed, if no other branches are chosen from the above sequence guide.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p>Drag questions to the left add rows, drag branches to the top add columns, right click on row or column headings to remove them.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.conditionalTreeTabs.setTabText(self.conditionalTreeTabs.indexOf(self.tab), QtGui.QApplication.translate("Form", "Sequence Guide", None, QtGui.QApplication.UnicodeUTF8))

