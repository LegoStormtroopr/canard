import sqblUI
import Canard_settings as settings
import isoLangCodes
from PyQt4 import QtCore, QtGui

class Dialog(QtGui.QDialog, sqblUI.preferencesDialog.Ui_CanardPreferencesDialog):
    def __init__(self):
        super(Dialog,self).__init__()
        self.setupUi(self)        
        self.tabWidget.setCurrentIndex(0) #Select the "Canard" Pane, means we can edit and save in QtDesigner on any tab as the active one, and still have the right one selected.
        self.setupDisplayLanguageCombo()
        self.setupDefaultLanguageList()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setupDisplayLanguageCombo(self):
        for code,title in isoLangCodes.languageCodeListPairs():
            self.defaultDisplayLanguage.addItem(title,code)
        self.defaultDisplayLanguage.insertSeparator(11) # insert after top 10
        langIndex = self.defaultDisplayLanguage.findData(settings.getPref('displayLanguage'))
        self.defaultDisplayLanguage.setCurrentIndex(max(0,langIndex))

    def setupDefaultLanguageList(self):
        self.possibleDefaultNewLangs.setSortingEnabled(True)
        self.defaultNewLangs.setSortingEnabled(True)
        for code,title in isoLangCodes.languageCodeListPairs(includeTopTen=False):
            item = QtGui.QListWidgetItem(title)
            item.setData(QtCore.Qt.UserRole,code)
            if code in settings.getPref('defaultObjectLangauges'):
                self.defaultNewLangs.addItem(item)
            else:
                self.possibleDefaultNewLangs.addItem(item)
        self.addDefaultNewLang.clicked.connect(self.addDefaultLang)
        self.removeDefaultNewLang.clicked.connect(self.removeDefaultLang)

    def addDefaultLang(self):
        self.fromListToList(self.possibleDefaultNewLangs,self.defaultNewLangs)
    def removeDefaultLang(self):
        self.fromListToList(self.defaultNewLangs,self.possibleDefaultNewLangs)
    def fromListToList(self,fromList,toList): 
        for item in fromList.selectedItems():
            row = fromList.row(item)
            toList.addItem(
                fromList.takeItem(row)
            )

    def accept(self):
        settings.setPref('displayLanguage',
            self.defaultDisplayLanguage.itemData(
                self.defaultDisplayLanguage.currentIndex()
            ).toPyObject()
        )

        settings.setPref('defaultObjectLangauges',
            [   str(self.defaultNewLangs.item(i).data(QtCore.Qt.UserRole).toPyObject())
                for i in range(self.defaultNewLangs.count())    ]
        )

        settings.setPref('checkForUpdates', self.checkForUpdates.isChecked())

        QtGui.QDialog.accept(self)

