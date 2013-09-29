import sqblUI
from PyQt4 import QtCore, QtGui
from SQBLmodel import _ns, _namespaces 
from lxml import etree
import isoLangCodes
#from repositoryDialog import repoDialog
import Canard_settings
import languagePicker

# Unfortunately not a hash because we want to keep this ordered consistantly in the UI
_comparisons = [
        ("="        , "equal_to" ),
        (u"\u2260"  , "not_equal_to" ),
        ("<"        , "less_than" ),
        (u"\u2264"  , "less_than_eq" ),
        (">"        , "greater_than" ),
        (u"\u2265"  , "greater_than_eq" ),
        ("includes" , "inclusive_of"),
        ("matches"  , "match_for"),
         ]

# A list of the currently allowed response types that Canard / SQBL support
responseTypes = ["Text","Number", "Code list"]

# Validator for valid names of objects
nameValidator = QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9_\-.]*"))

def comparisons():
    return _comparisons

# This maps tokens to the xml names for comparitors and vice versa
# Only strings should be passed here
def comparisonMap(tag):
    try:
        for token, xmlname in _comparisons:
            if tag == token:
                return xmlname
            if tag == xmlname:
                return token
    except:
        # if a comparison fails, we didnt get a string, so nothing will match, just return none.
        return None
    # You gave us a bad thing and there is no mapping. This could be an exception, but I'll let it slide for now.
    return None

# Returns all text and nodes under a given element with normalised spaces.
def getRichTextAsMarkup(tag):
    import re
    from lxml import objectify
    from copy import deepcopy
    tag = deepcopy(tag)
    text = tag.text
    if text is None:
        text = ""
    for e in tag:
        objectify.deannotate(e)
        etree.cleanup_namespaces(e)
        text += etree.tostring(e)
    text = text.strip()
    text = re.sub(r'xmlns=([\'"]).*?\1', ' ', text) # We don't need the namespace in the text editor
    text = re.sub(r'\s+', ' ', text)
    return text

class SQBLWidget(QtGui.QWidget):
    def __init__(self,element,model):
        QtGui.QWidget.__init__(self)
        # This should have been self.ui several thousand lines of code ago.
        self.setupUi(self)
        # TODO: Change above...
        self.element = element
        self.model = model

    def update(self,big=False):
        if big:
            self.model.emit(QtCore.SIGNAL('layoutChanged()'))
        self.model.emit(QtCore.SIGNAL('dataChanged()'))

#TODO: This seriously needs a better name moron
class SQBLWeirdThingWidget(SQBLWidget):
    # langXPath is the prefix for where to search for the langs from
    #   Above added so we didn't need to duplicate the below stuff for BulkQuestionEditors
    def __init__(self,element,model,langXPath=""):
        SQBLWidget.__init__(self,element,model)
        self.langXPathPrefix = langXPath

    # lang          - The language we want to change
    # newText       - The new Text for this element
    # parent        - The ETree Element that has the parent object of the TextComponent
    # textType      - The child element to update. If none, assumes the TextComponent is a simple textual field with no children
    def updateTextComponent(self,lang,newText,parent,textType=None):
        if lang is not None:
            lang = str(lang)
            elem = parent.xpath("s:TextComponent[@xml:lang='%s']"%(lang),namespaces=_namespaces)
            if len(elem) > 0:
                elem = elem[0]
            else:
                elem = etree.Element(_ns("s",'TextComponent'))
                elem.set("{%s}lang"%_namespaces['xml'],lang)
                parent.append(elem)
            if textType is None:
                elem.text = unicode(newText)
            else:
                field = elem.xpath("s:%s"%(textType),namespaces=_namespaces)
                if len(field) > 0:
                    field = field[0]
                else:
                    field = etree.Element(_ns("s",textType))
                    elem.append(field)
                field.text = unicode(newText)
            self.update()

    def configureLanguages(self,comboWidget,initialLanguage=None,interfaceLanguage="en"):
        cw = comboWidget #Just cause its easier to refer to
        langs = [] 
        for lang in self.element.xpath(self.langXPathPrefix+"s:TextComponent/@xml:lang",namespaces=_namespaces):
            if lang is not None and lang not in langs:
                langName = isoLangCodes.iso639CodeToString(lang)                
                cw.addItem(langName,lang)
                langs.append(lang)
        if len(langs) == 0:
            #There are no languages, so we'll add the curreent interface language to make sure something is there.
                langName = isoLangCodes.iso639CodeToString(interfaceLanguage)
                cw.addItem(langName,interfaceLanguage)


        self.languages.setCurrentIndex(-1)
        if initialLanguage is None: 
            self.languages.setCurrentIndex(0)
        else:
            langIndex = self.languages.findData(initialLanguage)
            self.languages.setCurrentIndex(max(0,langIndex))

    def connectAddRemoveLanguages(self,add,remove,languageCombo):
        def addLanguage():
            lang, success = languagePicker.Dialog()

            if success:
                index = languageCombo.findData(lang) # Check if language already listed
                if index == -1:
                    #If it doesn't, add it
                    langName = isoLangCodes.iso639CodeToString(lang)
                    languageCombo.addItem(langName,lang)
                    index = languageCombo.findData(lang) # Get the new index
                languageCombo.setCurrentIndex(index)
        add.clicked.connect(addLanguage)

class SQBLUnnamedWidget(SQBLWidget):
    def __init__(self,element,model,textType):
        SQBLWidget.__init__(self,element,model)
        self.textType = textType
        self.textLanguages = []
        self.activeLanguage = "en"

        # If its uses a "components" section use that, otherwise pull straight from the element
        newStyle = ["QuestionModule"]
        newStyle = [_ns("s",x) for x in newStyle] # Add namespaces
        if self.element.tag in newStyle:
            textCs = self.element.xpath("./s:TextComponents",namespaces=_namespaces)
            print "Has I got",self.element.tag
            if len(textCs) == 0:
                textCs = etree.Element(_ns("s","TextComponents"))
                self.element.insert(0,textCs)
            else:
                textCs = textCs[0]
        else:
            textCs = self.element
        self.texts = textCs
        for text in self.texts.xpath("./s:TextComponent",namespaces=_namespaces):
            self.textLanguages.append(text.get(_ns("xml","lang")))
        if self.activeLanguage not in self.textLanguages and len(self.textLanguages) > 0:
            self.activeLanguage = self.textLanguages[0]

        self.languagePicker = languagePicker.LanguagePickerWidget(
                    language=self.activeLanguage,
                    languages=sorted(self.textLanguages)
                )
        self.textLayout = self.textTab.layout()
        self.textLayout.addWidget(self.languagePicker)
        self.textLayout.setContentsMargins(1, 2, 2, 1)        
        self.textBox = None

        self.languagePicker.currentLanguageChanged.connect(self.changeLanguage)
        self.languagePicker.languageAdded.connect(self.addLanguage)
        self.languagePicker.languageRemoved.connect(self.removeLanguage)

        if len(self.textLanguages) == 0:
            newLang = unicode(Canard_settings.getPref('defaultObjectLangauge'))
            self.addLanguage(newLang)
        self.languagePicker.setLanguage(self.activeLanguage)

    def changeLanguage(self,lang):
        try:
            self.textLayout.removeWidget(self.textBox)
            oldText = self.textBox
            if oldText is not None:
                oldText.deleteLater()
        finally:
            text = self.texts.xpath("./s:TextComponent[@xml:lang='%s']"%lang,
                namespaces=_namespaces)[0]
            self.activeLanguage = str(lang)
            self.textBox = self.textType(text,self.model)

            self.textLayout.insertWidget(1,self.textBox)

    def addLanguage(self,lang):
        lang = str(lang)
        newText = etree.Element(_ns("s","TextComponent"))
        newText.set("{%s}lang"%_namespaces['xml'],lang)
        self.texts.insert(0,newText) # TextComponents are ALWAYS the first element, so we can just pop them up front

    def removeLanguage(self,lang):
        print lang
        elem = self.texts.xpath("./s:TextComponent[@xml:lang='%s']"%lang,
                namespaces=_namespaces)[0]
        elem.getparent().remove(elem)


# Node objects in the Module Logic, questions, conditionals, loops, etc...
# Ie. Things which have names and text components
class SQBLNamedWidget(SQBLUnnamedWidget):
    # We need the element itself, a reference to the model, and a class name for us to make the text component UI bits from
    def __init__(self,element,model,textType,tabWidget=None):
        SQBLUnnamedWidget.__init__(self,element,model,textType)

        self.nameChanged = False
        # We are now enforcing that the name UI Textfield for a node is ALWAYS called 'name'
        self.name.setText(self.element.get('name'))
        self.name.textChanged.connect(self.updateName)
        self.name.editingFinished.connect(self.callUpdates)
        

        def validated (text):
            state,length = nameValidator.validate(text,0)
            if state != QtGui.QValidator.Acceptable:
                pos = self.name.mapToGlobal(QtCore.QPoint(10,20))
                QtGui.QToolTip.showText(pos,"Names must start with a letter\n and contain only letters, numbers or underscores ")
            elif not self.model.isUniqueName(text):
                pos = self.name.mapToGlobal(QtCore.QPoint(10,20))
                QtGui.QToolTip.showText(pos,"Names must be unique")
            else:
                QtGui.QToolTip.hideText()

        def fixer ():
            state,length = nameValidator.validate(self.name.text(),0)
            text = self.name.text()
            acceptableText = False
            if state != QtGui.QValidator.Acceptable:
                pos = self.name.mapToGlobal(QtCore.QPoint(10,20))
                QtGui.QToolTip.showText(pos,"Names must start with a letter\n and contain only letters, numbers or underscores ")

            elif not self.model.isUniqueName(text):
                QtGui.QToolTip.showText(pos,"Names must be unique")
            else:
                acceptableText = True

            if not acceptableText:
                # The new name isn't accepatble, so we chomp it, and add a random number, this should be acceptable, and will prompt the user to change it.
                # TODO: Add a proper validation to make sure the new random name is acceptable. Its unlikely it won't be, but we want to make sure.
                from random import randint
                if len(text) > 25:
                    text = text[:25]
                text = str(text) + "_" + str(randint(10000,99999))
                self.name.setText(text[:32])

            

        self.name.textChanged.connect(validated)
        self.name.editingFinished.connect(fixer)
        self.name.setMaxLength(32)

    def callUpdates(self):
        if self.nameChanged:
            self.nameChanged = False
            self.update(big=True)

    def updateName(self):
        self.nameChanged = True
        newname = str(self.name.text())
        try:
            self.element.set('name',newname)
        except:
            pass
        self.update()

    # A helper method to do everything needed to connect the objects tabwidget to its preference methods.
    def connectTabPreferences(self,tabWidget):
        tabWidget.currentChanged.connect(self.setPrefTab)
        tabWidget.setCurrentIndex(self.getPrefTab())

    # Update the last selected tabs from a view
    def setPrefTab(self,index):
        pt = Canard_settings.getPref('PreferredTabs')
        if pt is None:
            pt = {}
        pt[type(self)] = index
        Canard_settings.setPref('PreferredTabs',pt)

    def getPrefTab(self):
        pt = Canard_settings.getPref('PreferredTabs')
        t = type(self)
        if pt is not None and t in pt.keys():
            return pt[t]
        return 0
    

class NewLanguageTab(QtGui.QWidget,sqblUI.newLanguageTab.Ui_Form):
    def __init__(self,parent):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.parent = parent

        common = []

        presentLangs = parent.texts.keys() #Languages that the element has
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
        self.languageList.addItems(common)
        self.languageList.insertSeparator(len(common))
        self.languageList.addItems(allLangs)
        self.addLanguage.clicked.connect(self.addNewLangauge)
        
    def addNewLangauge(self):
        element = self.parent.element
        newLang = unicode(self.languageList.currentText()[0:2]) # Get just the language code
        if newLang in self.parent.texts.keys():
            index = sorted(self.parent.texts.keys()).index(newLang)
        else:
            newText = etree.Element(_ns("s","TextComponent"))
            newText.set("{%s}lang"%_namespaces['xml'],newLang)
            element.append(newText)
            self.parent.texts[newLang] = self.parent.textType(newText,self.parent.model)
            index = sorted(self.parent.texts.keys()).index(newLang)
            self.parent.languageTabs.insertTab(index, self.parent.texts[newLang], newLang)
            self.languageList.removeItem(self.languageList.currentIndex())
        self.parent.languageTabs.setCurrentIndex(index)

# Below sourced from: http://www.yasinuludag.com/blog/?p=49
# Slight changes have been made for SQBL content
class XMLHighlighter(QtGui.QSyntaxHighlighter):
 
    #INIT THE STUFF
    def __init__(self, parent=None):
        super(XMLHighlighter, self).__init__(parent)
 
        self.highlightingRules = []

        xmlEm = QtGui.QTextCharFormat()
        xmlEm.setFontItalic(True)
        xmlEm.setForeground(QtCore.Qt.darkBlue)
        xmlEmRegex = QtCore.QRegExp("<em\s*>.*<\/em\s*>")
        xmlEmRegex.setMinimal(True)
        self.highlightingRules.append((xmlEmRegex, xmlEm))

        xmlWordSub = QtGui.QTextCharFormat()
        xmlWordSub.setFontWeight(QtGui.QFont.Bold)
        xmlWordSub.setForeground(QtCore.Qt.darkRed)
        xmlWordSubRegex = QtCore.QRegExp("<sub\s*.*\/>")
        xmlWordSubRegex.setMinimal(True)
        self.highlightingRules.append((xmlWordSubRegex, xmlWordSub))

 
    #VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING
    def highlightBlock(self, text):
 
        #for every pattern
        for pattern, format in self.highlightingRules:
 
            #Create a regular expression from the retrieved pattern
            expression = QtCore.QRegExp(pattern)
 
            #Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)
 
            #While the index is greater than 0
            while index >= 0:
 
                #Get the length of how long the expression is true, set the format from the start to the length with the text format
                length = expression.matchedLength()
                self.setFormat(index, length, format)
 
                #Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)
