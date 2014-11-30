# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/repositorySearch.ui'
#
# Created: Sun Nov 30 11:27:04 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(548, 323)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.retrievedItems = QtGui.QListWidget(Dialog)
        self.retrievedItems.setObjectName(_fromUtf8("retrievedItems"))
        self.gridLayout.addWidget(self.retrievedItems, 7, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 3)
        self.objectTypeLabel = QtGui.QLabel(Dialog)
        self.objectTypeLabel.setObjectName(_fromUtf8("objectTypeLabel"))
        self.gridLayout.addWidget(self.objectTypeLabel, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.objectType = QtGui.QComboBox(Dialog)
        self.objectType.setObjectName(_fromUtf8("objectType"))
        self.gridLayout.addWidget(self.objectType, 1, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(342, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.search = QtGui.QPushButton(Dialog)
        self.search.setObjectName(_fromUtf8("search"))
        self.gridLayout.addWidget(self.search, 3, 2, 1, 1)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 4, 0, 1, 3)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.searchTerms = QtGui.QLineEdit(Dialog)
        self.searchTerms.setObjectName(_fromUtf8("searchTerms"))
        self.gridLayout.addWidget(self.searchTerms, 2, 1, 1, 2)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.repositoryURLs = QtGui.QComboBox(Dialog)
        self.repositoryURLs.setEditable(True)
        self.repositoryURLs.setObjectName(_fromUtf8("repositoryURLs"))
        self.gridLayout.addWidget(self.repositoryURLs, 0, 1, 1, 2)
        self.line_2 = QtGui.QFrame(Dialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 8, 0, 1, 3)
        self.itemDetails = QtGui.QLabel(Dialog)
        self.itemDetails.setText(_fromUtf8(""))
        self.itemDetails.setWordWrap(True)
        self.itemDetails.setOpenExternalLinks(True)
        self.itemDetails.setObjectName(_fromUtf8("itemDetails"))
        self.gridLayout.addWidget(self.itemDetails, 9, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.objectTypeLabel.setText(QtGui.QApplication.translate("Dialog", "Object Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Repository Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.search.setText(QtGui.QApplication.translate("Dialog", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Results:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Search Terms:", None, QtGui.QApplication.UnicodeUTF8))

