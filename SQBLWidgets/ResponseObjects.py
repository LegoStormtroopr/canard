import sqblUI
from SQBLutil import * # Dont like this, need to fix later.

from PyQt4 import QtCore, QtGui
from SQBLmodel import _ns, _namespaces 
from lxml import etree
import isoLangCodes
import languagePicker

# We inherit from TextComponent, so we can reuse the connect method
class SQBLResponseObject(SQBLWeirdThingWidget):
    def __init__(self,element,model):
        SQBLWeirdThingWidget.__init__(self,element,model)

    # listOfFields is a dictonary, with 
    def connectToggle(self,UiField,tagName,defaultNew):
        def removeElement(state):
            if state == QtCore.Qt.Checked:
                self.element.append(defaultNew)
            elif state == QtCore.Qt.Unchecked:
                # Get rid of all matching tags, just to be sure.
                for i in self.element.xpath("./s:%s"%tagName,namespaces=_namespaces):
                    self.element.remove(i)
            else:
                # This checkbox has only 2 states, if we end up here, something terribly bad has happened
                raise Exception('QtCheckStateError', 'Response Toggle in 3rd state.')
            self.update()

        return removeElement 

    def connectMLFields(self,hintValueField,tagname,langPicker):
        def updateTagName(text):
            lang = langPicker.itemData(langPicker.currentIndex()).toPyObject()
            elem = self.element.xpath("./s:%s" % (tagname),namespaces=_namespaces)[0]
            self.updateTextComponent(lang,text,elem)

        # This function updates the value of this text box if the language picker changes
        def updateField(index):
            lang = str(langPicker.itemData(index).toPyObject())
            text = self.element.xpath("./s:%s/s:TextComponent[@xml:lang='%s']" % (tagname,lang),namespaces=_namespaces)
            value = ""
            if len(text) > 0:
                value = text[0].text
            if hintValueField.isEnabled():
                hintValueField.setText(value)
            self.update()

        hintValueField.textChanged.connect(updateTagName)
        #hintValueField.textChanged.connect(updateTagName)
        langPicker.currentIndexChanged[int].connect(updateField)

    def connectValueFields(self,tagname,valueField):
        def changed(value):
            if valueField.isEnabled():
                tag = self.element.xpath("./s:%s" % (tagname),namespaces=_namespaces)[0]
                tag.set("value", str(value))
        valueField.valueChanged.connect(changed)

    def initialiseRestraintFields(self,tagname,defaultElement,checkbox,languageCombo,textField=None,valueField=None):
        
        toggleMethod = self.connectToggle(checkbox,tagname,defaultElement)

        # Here we initialise the checkbox
        elem = self.element.xpath("./s:%s" % (tagname),namespaces=_namespaces)
        state = QtCore.Qt.Unchecked
        if len(elem) > 0:
            state = QtCore.Qt.Checked
            if valueField is not None:
                valueField.setValue(float(elem[0].get('value')))
        checkbox.setCheckState(state)

        if textField is not None:
           self.connectMLFields(textField,tagname,languageCombo)
        if valueField is not None:
            self.connectValueFields(tagname,valueField)
        checkbox.stateChanged.connect(toggleMethod)

    # Connect the minimum and maximum fields so they bound each others values correctly.
    # The fixed minimum is a value that can be optionally set as the "smallest value for this field", useful for lengths.
    def connectMinMax(self,minimum,maximum,minCheck,maxCheck,fixedMinimum=None):
        # Qt thinks these are very large numbers. Lets not disagree
        if fixedMinimum is None:
            fixedMinimum = -16777215
        fixedMaximum = 16777215
        
        def setMin(minValue):
            if minimum.isEnabled():
                maximum.setMinimum(minValue)
                maximum.setValue(0)
        minimum.valueChanged.connect(setMin)

        def setMax(maxValue):
            if maximum.isEnabled():
                minimum.setMaximum(maxValue)
                minimum.setValue(0)
        maximum.valueChanged.connect(setMax)

        def unsetMin(enabled):
            maximum.setMinimum(fixedMinimum)
        minCheck.toggled.connect(unsetMin)

        def unsetMax(enabled):
            minimum.setMaximum(fixedMaximum)
        maxCheck.toggled.connect(unsetMax)

class CodeList(SQBLResponseObject, sqblUI.responseCodeList.Ui_Form):
    def __init__(self,element,model):
        SQBLResponseObject.__init__(self,element,model)

        self.initialiseRestraintFields( tagname = "MinimumSelections",
                defaultElement = etree.fromstring("<MinimumSelections xmlns='%s' value='1' />"% _namespaces['s']),
                checkbox = self.hasMinSelections,
                languageCombo = self.languages,
                textField = self.minSelectionsHint,
                valueField = self.minSelections
            )

        self.initialiseRestraintFields( tagname = "MaximumSelections",
                defaultElement = etree.fromstring("<MaximumSelections xmlns='%s' value='1' />"% _namespaces['s']),
                checkbox = self.hasMaxSelections,
                languageCombo = self.languages,
                textField = self.maxSelectionsHint,
                valueField = self.maxSelections
            )

        self.connectAddRemoveLanguages(self.addLanguage,self.removeLanguage,self.languages)
        self.prepCodeListBox()
        self.languages.currentIndexChanged[int].connect(self.updateCodeListTable)
        self.configureLanguages(self.languages)
        self.codeListTable.cellChanged.connect(self.updateCell)
        self.codeListTable.resizeColumnsToContents()
        self.addCode.clicked.connect(self.addCodeToList)
        self.removeCode.clicked.connect(self.removeCodeFromList)

        # Connects for allowing reordering of Branch columns conditionals
        self.codeListTable.verticalHeader().setMovable(True)
        self.codeListTable.verticalHeader().sectionMoved.connect(self.reorderCode)

        header = self.codeListTable.verticalHeader()
        header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.popup)

    # Create pop up menu for deleting codes.
    def popup(self, pos):
        header = self.codeListTable.verticalHeader()
        menu = QtGui.QMenu()
        deleteAction = menu.addAction("Delete Code")
        action = menu.exec_(header.mapToGlobal(pos))
        if action == deleteAction:
            self.removeCodeFromList(index = header.visualIndex(header.logicalIndexAt(pos)))

    # Where its stored, where it did appear, where it appears now
    def reorderCode(self,logicalIndex,oldVisIndex,newVisIndex):
        codelist =  self.element.xpath("./s:Codes",namespaces=_namespaces)[0] #there can be only one
        codepairs = codelist.xpath("./s:CodePair",namespaces=_namespaces)
        movedCode = codepairs[oldVisIndex]
        codelist.insert(newVisIndex,movedCode)
        self.update()

    def addCodeToList(self):
        #row = self.codeListTable.rowCount()
        # Insert before the first selected row
        rows =  [i.row() for i in self.codeListTable.selectionModel().selectedRows()]
        rows.sort()
        rows.append(self.codeListTable.rowCount()) #Ensure we always have a value
        row = rows[0]
        self.codeListTable.insertRow(row)

        # Add new XML Node
        codes = self.element.xpath(".//s:Codes",namespaces=_namespaces)[0] 
        newCodePair = etree.Element(_ns("s",'CodePair'))
        newCodePair.set('code', "")
        codes.insert(row,newCodePair) #Don't have to add 1, as lXML is smart.

        # Make checkbox field
        item = QtGui.QTableWidgetItem('')
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.codeListTable.setItem(row,1,item)

        self.update() 

    def removeCodeFromList(self,index = None):
        if index is None or index is False:
            rows =  [i.row() for i in self.codeListTable.selectionModel().selectedRows()]
            rows.sort(); rows.reverse()
        else:
            rows = [index]
        for row in rows:
            self.codeListTable.removeRow(row)
            codePair = self.element.xpath(".//s:Codes/s:CodePair[position()=%s]"%(row+1),namespaces=_namespaces)[0] #Add one because XML positions are indexed from 1. DAMN IT.
            codePair.getparent().remove(codePair)
        self.update() 

    def updateCell(self,row,col):
        codePair = self.element.xpath(".//s:Codes/s:CodePair[position()=%s]"%(row+1),namespaces=_namespaces)[0] #Add one because XML positions are indexed from 1. DAMN IT.
        if col == 0: # Code Value column
            #codePair.set('code',
            #        self.codeListTable.item(row,col).checkState()  == QtCore.Qt.Checked)
            print self.codeListTable.item(row,col).text()
            codePair.set('code', unicode(self.codeListTable.item(row,col).text()))

        elif col == 1: # Checkbox column 
            if self.codeListTable.item(row,col).checkState() == QtCore.Qt.Checked:
                codePair.set('freeText', 'true')
            else:
                # If its not freeText, just remove it for cleaner XML
                if "freeText" in codePair.attrib.keys():
                    codePair.attrib.pop('freeText')

        elif col == 2: # Text Column
            lang = str(self.languages.itemData(self.languages.currentIndex()).toPyObject())
            text = unicode(self.codeListTable.item(row,col).text())
            self.updateTextComponent(lang,text,codePair)

        self.update() 

    def updateCodeListTable(self,index):
        lang = str(self.languages.itemData(index).toPyObject())
        for row,codePair in enumerate(self.element.xpath(".//s:Codes/s:CodePair",namespaces=_namespaces)):
            text = codePair.xpath("./s:TextComponent[@xml:lang='%s']" % (lang),namespaces=_namespaces)
            if len(text) > 0:
                # The language is in the XML so add it in
                text = ' '.join(text[0].text.split()) #Why python, WHY??
            else:
                # We haven't got text in the language, so just blank the box.
                text = "" 
            self.codeListTable.setItem(row,2,QtGui.QTableWidgetItem(text))
        #self.update()

    def prepCodeListBox(self,lang="en"):
        #self.codeListTable.clearContents() #inefficient, but good enough for a MVP
        self.codeListTable.setColumnCount(3)
        for row,codePair in enumerate(self.element.xpath(".//s:Codes/s:CodePair",namespaces=_namespaces)):
            self.codeListTable.setRowCount(row+1)
            code = codePair.get('code')
            isFreeText = codePair.get('freeText') == "true" #The default is false, so if not explicitly true, it must be false.
            self.codeListTable.setItem(row,0,QtGui.QTableWidgetItem(code))

            # Add check boxes for free text fields
            item = QtGui.QTableWidgetItem('')
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if isFreeText:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.codeListTable.setItem(row,1,item)
        

class Number(SQBLResponseObject, sqblUI.responseNumber.Ui_Form):
    def __init__(self,element,model):
        SQBLResponseObject.__init__(self,element,model)

        self.initialiseRestraintFields( tagname = "Minimum",
                defaultElement = etree.fromstring("<Minimum xmlns='%s' value='0' />"% _namespaces['s']),
                checkbox = self.hasMinValue,
                languageCombo = self.languages,
                textField = self.minValueHint,
                valueField = self.minValue
            )

        self.initialiseRestraintFields( tagname = "Step",
                defaultElement = etree.fromstring("<Step xmlns='%s' value='0' />"% _namespaces['s']),
                checkbox = self.hasStepValue,
                languageCombo = self.languages,
                textField = self.stepValueHint,
                valueField = self.stepValue
            )

        self.initialiseRestraintFields( tagname = "Maximum",
                defaultElement = etree.fromstring("<Maximum xmlns='%s' value='0' />"% _namespaces['s']),
                checkbox = self.hasMaxValue,
                languageCombo = self.languages,
                textField = self.maxValueHint,
                valueField = self.maxValue
            )

        self.initialiseRestraintFields( tagname = "Hint",
                defaultElement = etree.fromstring("<Hint xmlns='%s' />"% _namespaces['s']),
                checkbox = self.hasDisplayHint,
                languageCombo = self.languages,
                textField = self.displayHint,
            )

        self.initialiseRestraintFields( tagname = "Prefix",
                defaultElement = etree.fromstring("<Prefix xmlns='%s' />"% _namespaces['s']),
                checkbox = self.hasPrefix,
                languageCombo = self.languages,
                textField = self.prefix,
            )

        self.initialiseRestraintFields( tagname = "Suffix",
                defaultElement = etree.fromstring("<Suffix xmlns='%s' />"% _namespaces['s']),
                checkbox = self.hasSuffix,
                languageCombo = self.languages,
                textField = self.suffix,
            )

        self.connectMinMax(minimum=self.minValue,
                maximum=self.maxValue,
                minCheck = self.hasMinValue,
                maxCheck = self.hasMaxValue
                )

        # Do this as a last step, to select a display language
        self.connectAddRemoveLanguages(self.addLanguage,self.removeLanguage,self.languages)
        self.configureLanguages(self.languages)

class Text(SQBLResponseObject, sqblUI.responseText.Ui_Form):
    def __init__(self,element,model):
        SQBLResponseObject.__init__(self,element,model)

        self.initialiseRestraintFields( tagname = "MinimumLength",
                defaultElement = etree.fromstring("<MinimumLength xmlns='%s' value='0' />"% _namespaces['s']),
                checkbox = self.hasMinLength,
                languageCombo = self.languages,
                textField = self.minLengthHint,
                valueField = self.minLengthValue
            )

        self.initialiseRestraintFields( tagname = "MaximumLength",
                defaultElement = etree.fromstring("<MaximumLength xmlns='%s' value='0' />"% _namespaces['s']),
                checkbox = self.hasMaxLength,
                languageCombo = self.languages,
                textField = self.maxLengthHint,
                valueField = self.maxLengthValue
            )

        self.initialiseRestraintFields( tagname = "Hint",
                defaultElement = etree.fromstring("<Hint xmlns='%s' />"% _namespaces['s']),
                checkbox = self.hasDisplayHint,
                languageCombo = self.languages,
                textField = self.displayHint,
            )

        self.connectMinMax(minimum=self.minLengthValue,
                maximum=self.maxLengthValue,
                minCheck = self.hasMinLength,
                maxCheck = self.hasMaxLength
                )

        self.connectAddRemoveLanguages(self.addLanguage,self.removeLanguage,self.languages)
        self.configureLanguages(self.languages)

