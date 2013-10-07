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
        self.defaultDisplayLanguage.insertSeparator(10)
        langIndex = self.defaultDisplayLanguage.findData(settings.getPref('displayLangauge'))
        self.defaultDisplayLanguage.setCurrentIndex(max(0,langIndex))

    def setupDefaultLanguageList(self):
        for code,title in isoLangCodes.languageCodeListPairs():
            if code not in settings.getPref('defaultObjectLangauges'):
                self.possibleDefaultNewLangs.addItem(title)
        

    def accept(self):
        settings.setPref('displayLangauge',
            self.defaultDisplayLanguage.itemData(
                self.defaultDisplayLanguage.currentIndex()
            ).toPyObject()
        )

        QtGui.QDialog.accept(self)

