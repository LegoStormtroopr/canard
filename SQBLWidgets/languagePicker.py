import sqblUI
from SQBLutil import * # Dont like this, need to fix later.
from PyQt4 import QtGui, QtCore
import isoLangCodes
from lxml import etree

def Dialog(title = "Enter Language", default = None):
    common = []
    for code,data in isoLangCodes.popularcodes.items():
        common.append(code + " - " + data['name'] + " / " + data['native'])
    common.sort()
    allLangs = []
    for code,data in isoLangCodes.langcodes.items():
        try:
            allLangs.append("" + code + " - " + data['name'] + " / " + data['native'])
        except:
            allLangs.append("" + code + " - ")
    allLangs.sort()

    names = [""] + common + allLangs
    lang,success = QtGui.QInputDialog.getItem(None,
        title,
        """Enter a <a href='http://en.wikipedia.org/wiki/ISO_639 '>2 letter ISO 639 Language Code ID</a>,<br>or select a common country from the list.<br>
            <br>
            This list of languages was selected from the <a href="en.wikipedia.org/wiki/Global_Internet_usage#Internet_users_by_language">Top 10 langauges used on the Internet</a>.<br>
            American English was added, due to the large number of native users within Information Technology.""",
        names,
        current = 0,
        editable = False,
        )
    if success:
        # The entered a language successfully, good for them.
        lang = lang[0:2]
        lang = unicode(lang)
    return (lang,success)
        

class LanguagePickerWidget(QtGui.QWidget,sqblUI.languagePicker.Ui_Form):

    # Signal emitted if current language in the language combo box changes
    # String emitted is an iso639 code
    currentLanguageChanged = QtCore.pyqtSignal(str)

    # String emitted is an iso639 code
    languageAdded = QtCore.pyqtSignal(str)

    # String emitted is an iso639 code
    languageRemoved = QtCore.pyqtSignal(str)

    # language and languages are iso639 languages codes
    def __init__(self,language=None,languages=[],hideLabel=False):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.currentLanguage = language
        languages.append(language)
        self.languages = sorted(list(set(languages)))
        self.configureLanguages(self.languageList)
        
        self.addLanguageButton.clicked.connect(self.addLanguage)
        self.removeLanguageButton.clicked.connect(self.removeLanguage)

        self.languageList.currentIndexChanged[int].connect(self.updateLanguage)
        if language in self.languages:
            self.languageList.setCurrentIndex(self.languages.index(language))
        else:
            self.languageList.setCurrentIndex(0)
        

    def removeLanguage(self):
        pass
        index = self.languageList.currentIndex()
        lang = self.languageList.itemData(index)
        self.languages.remove(lang)
        self.languageList.removeItem(index)
        self.languageRemoved.emit(lang.toPyObject())

    def addLanguage(self,lang):
        lang, success = languagePickerDialog()
        if lang is None or lang == "":
            return
        lang = str(lang)
        if success and lang not in self.languages:

            self.languageAdded.emit(lang)
            self.languages.append(lang)
            self.languages.sort()
            self.languageList.addItem(isoLangCodes.iso639CodeToString(lang),lang)
        if lang in self.languages:
            self.languageList.setCurrentIndex(self.languageList.findData(lang))

    def setLanguage(self,language):
        if language in self.languages:
            self.languageList.setCurrentIndex(self.languages.index(language))
            self.updateLanguage(self.languages.index(language))

    def updateLanguage(self,index):
        self.currentLanguage = str(self.languageList.itemData(index).toPyObject())
        self.currentLanguageChanged.emit(self.currentLanguage)

    def configureLanguages(self,comboWidget,interfaceLanguage="en"):
        cw = comboWidget #Just cause its easier to refer to
        for lang in self.languages:
            langName = isoLangCodes.iso639CodeToString(lang)                
            cw.addItem(langName,lang)
        if len(self.languages) == 0:
            #There are no languages, so we'll add the current interface language to make sure something is there.
            cw.addItem(interfaceLanguage)

        langIndex = self.languageList.findData(self.currentLanguage)
        self.languageList.setCurrentIndex(max(0,langIndex))

