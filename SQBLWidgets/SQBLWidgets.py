import sqblUI
from SQBLutil import * # Dont like this, need to fix later.

from PyQt4 import QtCore, QtGui
import SQBLmodel
from SQBLmodel import _ns, _namespaces 
from lxml import etree
import isoLangCodes
#from repositoryDialog import repoDialog
import Canard_settings
import ResponseObjects as Responses
import SQBLutil
import languagePicker

# If we don't have interfaces and such, lets just show a very unhelpful error message :/
class UnsupportedWidget(SQBLWidget,sqblUI.unsupportedWidget.Ui_Form):
    def __init__(self):
        SQBLWidget.__init__(self,None,None)

class WordSubstitutions(SQBLWidget,sqblUI.wordSubstitutions.Ui_Form):
    def __init__(self):
        SQBLWidget.__init__(self,None,None)

class DerivedDataItems(SQBLWidget,sqblUI.derivedDataItems.Ui_Form):
    def __init__(self):
        SQBLWidget.__init__(self,None,None)

class BulkQuestionEditor(SQBLWeirdThingWidget, sqblUI.bulkQuestionEditor.Ui_Form):
    def __init__(self,element,model):
        SQBLWeirdThingWidget.__init__(self,element,model,langXPath="//")
        self.prepQuestionList()
        self.languages.currentIndexChanged[int].connect(self.updateQuestionList)
        self.configureLanguages(self.languages)
        self.questionList.cellChanged.connect(self.updateCell)
        self.addAction(self.actionAddQuestion)
        self.questionList.cycleFromLastCell.connect(self.newQuestion)

    def prepQuestionList(self):
        rows = len(self.element.xpath("//s:Question",namespaces=_namespaces))
        self.questionList.setRowCount(rows)

    def updateQuestionList(self,index):
        lang = str(self.languages.itemData(index).toPyObject())
        self.questionList.clearContents()
        for row,q in enumerate(self.element.xpath("//s:Question",namespaces=_namespaces)):
            # Set the question name
            name = q.get("name")
            idCell = QtGui.QTableWidgetItem(name)
            idCell.setData(32,name) #Set the name so we can find it again when it changes
            self.questionList.setItem(row,0,idCell)

            text = q.xpath("./s:TextComponent[@xml:lang='%s']/s:QuestionText" % (lang),namespaces=_namespaces)
            if len(text) > 0:
                text = SQBLutil.getRichTextAsMarkup(text[0])
            else:
                text = "" 
            combo = QtGui.QComboBox(self)

            # Allowed responses for the combo box
            allowedResponses = SQBLutil.responseTypes
            possibleReponseOptions = allowedResponses 
            option = 'Unknown' # The final option to select

            # Actual responses in the question
            responses = q.xpath("s:ResponseType/*",namespaces=_namespaces) 
            if len(responses) > 1:
                # Its got a multiple mixed responses, lets not let the user ruin that
                possibleReponseOptions += ['Mixed'] 
                option = 'Mixed'
                combo.setEnabled(False) 
                combo.setToolTip("Locked, for your protection")
            else:
                responseTag = responses[0].tag.split('}',1)[1] # Get just the tag name
                if responseTag in allowedResponses:
                    # Its probably ok to let the user change these.
                    option = responseTag
            if option == 'Unknown':
                # We don't know what type it is, set it to unknown and lock it
                possibleReponseOptions += ['Unknown'] 
                combo.setEnabled(False) 
                combo.setToolTip("Locked, for your protection")
                
            for response in possibleReponseOptions:
                combo.addItem(response)
            combo.setCurrentIndex(possibleReponseOptions.index(option))
            self.questionList.setCellWidget(row,1,combo)
            self.questionList.setItem(row,2,QtGui.QTableWidgetItem(text))

    def newQuestion(self):
        # TODO: When a user hits enter in the last question we should add a new one easily
        pass

    def updateCell(self,row,col):
        qID = self.questionList.item(row,0).data(32).toPyObject() # Get the original ID in case it changed
        q = self.element.xpath("//s:Question[@name='%s']"%(qID),namespaces=_namespaces)[0]
        text = unicode(self.questionList.item(row,col).text())
        lang = self.languages.itemData(self.languages.currentIndex()).toPyObject()

        if col == 0:
            # Changing the ID, so let the model handle this
            self.model.changeName(qID,text)
        if col == 0:
            # Changing the response type
            pass
        elif col == 2:
            # Changing the QuestionText
            self.updateTextComponent(lang,text,q,textType="QuestionText")
        else:
            pass
            #self.updateTextComponent(lang,text,subQ)

        self.update() 

class ModuleLogic(SQBLNamedWidget, sqblUI.moduleLogic.Ui_Form):
    def __init__(self,element,model):
        SQBLWidget.__init__(self,element,model)
        self.bulkQEditor = BulkQuestionEditor(element,model)
        self.tabBulkQuestionEditor.layout().addWidget(self.bulkQEditor)

class QuestionGroup(SQBLNamedWidget, sqblUI.questionGroup.Ui_Form):
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,QuestionText)

class LoopFor(SQBLNamedWidget, sqblUI.loopFor.Ui_Form):
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,LogicNodeText)

        self.initialiseLoopQuestionReference()

    def initialiseLoopQuestionReference(self):

        for name,text in self.model.findQuestions(lang="en"):
            self.loopQuestionCombo.addItem("%s - %s "%(name,text),name)
        index = self.loopQuestionCombo.findData(self.element.get("question")) # Get the new index
        self.loopQuestionCombo.setCurrentIndex(index)
        self.loopQuestionCombo.currentIndexChanged[int].connect(self.updateLoopQuestionReference)

    def updateLoopQuestionReference(self,index):
        self.element.set("question",str(self.loopQuestionCombo.itemData(index).toPyObject()))
        self.update(big=True)


class Branch(SQBLNamedWidget, sqblUI.branch.Ui_Form):
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,LogicNodeText)

class QuestionModule(SQBLNamedWidget, sqblUI.questionModule.Ui_Form):
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,QuestionModuleText)

class SubQuestion(SQBLWeirdThingWidget, sqblUI.subQuestion.Ui_Form):
    def __init__(self,element,model):
        SQBLWeirdThingWidget.__init__(self,element,model)

        subQs = self.element.xpath(".//s:SubQuestions",namespaces=_namespaces)
        if len(subQs) == 0:
            subQs = None
        else:
            subQs = subQs[0]
        self.subQuestions = subQs

        self.connectAddRemoveLanguages(self.addLanguage,self.removeLanguage,self.languages)
        self.languages.currentIndexChanged[int].connect(self.updateSubQuestionList)
        self.prepSubQuestionList()
        self.subQuestionList.cellChanged.connect(self.updateCell)

        self.addSubQuestionBtn.clicked.connect(self.addSubQuestion)
        self.removeSubQuestionBtn.clicked.connect(self.removeSubQuestion)

        # Connects for allowing reordering of Branch columns conditionals
        self.subQuestionList.verticalHeader().setMovable(True)
        self.subQuestionList.verticalHeader().sectionMoved.connect(self.reorderSubQuestions)

        self.configureLanguages(self.languages)

    # Where its stored, where it did appear, where it appears now
    def reorderSubQuestions(self,logicalIndex,oldVisIndex,newVisIndex):
        subQs = self.subQuestions.xpath("./s:SubQuestion",namespaces=_namespaces)
        movedSubQ = subQs[oldVisIndex]
        self.subQuestions.insert(newVisIndex,movedSubQ)
        self.update()

    def addSubQuestion(self):
        rows =  [i.row() for i in self.subQuestionList.selectionModel().selectedRows()]
        rows.sort()
        rows.append(self.subQuestionList.rowCount()) #Ensure we always have a value
        row = rows[0] 
        self.subQuestionList.insertRow(row)

        if self.subQuestions == None:
            self.subQuestions = etree.Element(_ns("s",'SubQuestions'))
            self.element.append(self.subQuestions)
            self.removeSubQuestionBtn.setEnabled(True)
        newSubQuestion = etree.Element(_ns("s",'SubQuestion'))
        self.subQuestions.insert(row,newSubQuestion)
        self.update() 

    def removeSubQuestion(self,index = None):
        if index is None or index is False:
            rows =  [i.row() for i in self.subQuestionList.selectionModel().selectedRows()]
            rows.sort(); rows.reverse()
        else:
            rows = [index]
        for row in rows:
            self.subQuestionList.removeRow(row)
            subQ = self.subQuestions.xpath("s:SubQuestion",namespaces=_namespaces)[row] 
            self.subQuestions.remove(subQ)

        if self.subQuestionList.rowCount() == 0:
            # No more subquestions, lets remove out optional element.
            old = self.subQuestions
            self.element.remove(old)
            self.subQuestions = None
            self.removeSubQuestionBtn.setEnabled(False)
            
        self.update() 
        
    def updateCell(self,row,col):
        subQ = self.element.xpath(".//s:SubQuestions/s:SubQuestion[position()=%s]"%(row+1),namespaces=_namespaces)[0] #Add one because XML positions are indexed from 1. DAMN IT.

        lang = self.languages.itemData(self.languages.currentIndex()).toPyObject()
        text = unicode(self.subQuestionList.item(row,col).text())
        self.updateTextComponent(lang,text,subQ)

        self.update() 

    def prepSubQuestionList(self,lang="en"):
        rows = len(self.element.xpath(".//s:SubQuestions/s:SubQuestion",namespaces=_namespaces))
        self.subQuestionList.setColumnCount(1)        
        self.subQuestionList.setRowCount(rows)

    def updateSubQuestionList(self,index):
        lang = str(self.languages.itemData(index).toPyObject())
        self.subQuestionList.clearContents()
        for row,subQ in enumerate(self.element.xpath(".//s:SubQuestions/s:SubQuestion",namespaces=_namespaces)):
            text = subQ.xpath("./s:TextComponent[@xml:lang='%s']" % (lang),namespaces=_namespaces)
            if len(text) > 0:
                text = text[0].text
            else:
                text = "" 
            
            self.subQuestionList.setItem(row,0,QtGui.QTableWidgetItem(text))


    
class Question(SQBLNamedWidget, sqblUI.question.Ui_Form):
    # We need the XML object, and the model so we can make change calls.
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,QuestionText)

        # Connect Data Element updaters
        deURL = self.element.get('dataElementReference')
        if deURL is None:
            deURL = ""
        self.dataElementURI.setText(deURL)
        self.dataElementURI.textChanged.connect(self.changeDataElementURI)
        self.dataElementURI.editingFinished.connect(self.update)
        #Allow for display of data element preview
        self.previewDataElementPage.clicked.connect(self.previewDataElement)
        self.openDataElementInBrowser.clicked.connect(self.openInBrowser)

        # QWebView has a wierd resize issue where it forces itself to be too big playing havok with layout. Lets fix that...

        # Configure subQuestionTab

        self.subQuestionPane = SubQuestion(self.element,model)
        self.subQuestionsTab.layout().addWidget(self.subQuestionPane)

        responseTypes = SQBLutil.responseTypes
        self.responses = self.element.xpath("./s:ResponseType",namespaces=_namespaces)[0]
        #self.responseType.addItems(responseTypes)

        #self.responseType.currentIndexChanged.connect(self.changeResponseType)
        #self.responsePlaceHolder.addWidget(self.responseField)
        
        # Below will only be true if the value in the XML is 'true' i.e. XML Boolean true.
        self.canRefuse.setChecked(self.responses.get("canRefuse",False)=='true')
        self.canRefuse.toggled.connect(self.setCanRefuse)
        self.canDontKnow.setChecked(self.responses.get("canDontKnow",False)=='true')
        self.canDontKnow.toggled.connect(self.setCanDontKnow)
        self.updateTargetPopulation()
        self.setupResponseTabs()

        self.responseTabs.tabBar().tabMoved.connect(self.reorderResponse)
        self.questionTabs.currentChanged.connect(self.setPrefTab)
        self.questionTabs.setCurrentIndex(self.getPrefTab())

    def reorderResponse(self,tabTo,tabFrom):
        movedResponse = self.responses.xpath("./*",namespaces=_namespaces)[tabFrom]
        self.responses.insert(tabTo,movedResponse)
        self.update()


    def addBooleanResponse(self):
        element = etree.Element("{%s}Boolean"%(_namespaces['s']))
        self.responses.append(element)
        responseField = Responses.Boolean(element,self.model) 
        self.responseTabs.addTab(responseField,"Boolean")

    def addDateResponse(self):
        element = etree.Element("{%s}Date"%(_namespaces['s']))
        self.responses.append(element)
        responseField = Responses.Date(element,self.model) 
        self.responseTabs.addTab(responseField,"Date")

    def addNumericResponse(self):
        element = etree.Element("{%s}Number"%(_namespaces['s']))
        self.responses.append(element)
        responseField = Responses.Number(element,self.model) 
        self.responseTabs.addTab(responseField,"Number")

    def addTextResponse(self):
        element = etree.Element("{%s}Text"%(_namespaces['s']))
        self.responses.append(element)
        responseField = Responses.Text(element,self.model) 
        self.responseTabs.addTab(responseField,"Text")

    def addTimeResponse(self):
        element = etree.Element("{%s}Time"%(_namespaces['s']))
        self.responses.append(element)
        responseField = Responses.Time(element,self.model) 
        self.responseTabs.addTab(responseField,"Time")

    def addCodeListResponse(self):
        element = etree.fromstring("""
          <CodeList xmlns="%s">
            <Codes />
          </CodeList>
        """%(_namespaces['s']))
        self.responses.append(element)
        responseField = Responses.CodeList(element,self.model) 
        self.responseTabs.addTab(responseField,"CodeList")

    def setupResponseTabs(self):
        # Add Response Button
        arb = QtGui.QToolButton(self.responseTabs)
        arb.setText("Add... ")
        arb.setAutoRaise(True)
        arb.setPopupMode(QtGui.QToolButton.InstantPopup)

        arbMenu = QtGui.QMenu("Add Response", arb)
        addBool = arbMenu.addAction("Boolean Response")
        addDate = arbMenu.addAction("Date Response")
        addCode = arbMenu.addAction("CodeList Response")
        addNum  = arbMenu.addAction("Numeric Response")
        addText = arbMenu.addAction("Text Response")
        addTime = arbMenu.addAction("Time Response")
        
        addBool.triggered.connect(self.addBooleanResponse)
        addCode.triggered.connect(self.addCodeListResponse)
        addDate.triggered.connect(self.addDateResponse)
        addNum.triggered.connect(self.addNumericResponse)
        addText.triggered.connect(self.addTextResponse)
        addTime.triggered.connect(self.addTimeResponse)
        arb.setMenu(arbMenu)

        self.responseTabs.setCornerWidget(arb)
        for response in self.responses:
            responseField = None
            if response.tag == _ns("s","CodeList"):
                responseField = Responses.CodeList(response,self.model) 
                #self.responseType.setCurrentIndex(2)
                tabName = "Codelist"
            elif response.tag == _ns("s","Date"):
                responseField = Responses.Date(response,self.model) 
                #self.responseType.setCurrentIndex(1)
                tabName = "Date"
            elif response.tag == _ns("s","Number"):
                responseField = Responses.Number(response,self.model) 
                #self.responseType.setCurrentIndex(1)
                tabName = "Number"
            elif response.tag == _ns("s","Text"):
                responseField = Responses.Text(response,self.model) 
                #self.responseType.setCurrentIndex(0)
                tabName = "Text"
            elif response.tag == _ns("s","Time"):
                responseField = Responses.Time(response,self.model) 
                #self.responseType.setCurrentIndex(1)
                tabName = "Time"
            elif response.tag == _ns("s","Boolean"):
                responseField = Responses.Boolean(response,self.model) 
                #self.responseType.setCurrentIndex(0)
                tabName = "Boolean"
            if responseField is not None:
                self.responseTabs.addTab(responseField,tabName)
        self.responseTabs.tabCloseRequested.connect(self.removeResponse)

    def removeResponse(self,index):
        h = self.responseTabs.cornerWidget().height()
        self.responses.remove(self.responseTabs.widget(index).element)
        self.responseTabs.removeTab(index)
        self.update()
        if len(self.responses) == 0:
            self.responseTabs.cornerWidget().setMinimumHeight(h)
            self.responseTabs.setMinimumHeight(h)

    def changeDataElementURI(self):
        self.element.set('dataElementReference',
            str(self.dataElementURI.text())
          )

    def previewDataElement(self):
        self.dataElementPagePreview.setUrl(QtCore.QUrl(self.dataElementURI.text()))

    def openInBrowser(self):
        import webbrowser
        webbrowser.open(str(self.dataElementURI.text()))

    # This is a deprecated function from when we 'constructed' the data element.
    # It may be useful for registry searches later.
    def changeObjectClass(self):
        dlg = repoDialog(self,objectType="ObjectClass")
        if dlg.exec_():
            values = dlg.getValues()

    def setCanRefuse(self,canRefuse):
        if canRefuse:
            self.response.set('canRefuse','true')
        else:
            self.response.attrib.pop('canRefuse')
        self.update()

    def setCanDontKnow(self,canDontKnow):
        if canDontKnow:
            self.response.set('canNotKnow','true')
        else:
            self.response.attrib.pop('canNotKnow')
        self.update()

    def updateTargetPopulation(self):
        text = ""
        for i,a in enumerate([ a for a in self.element.iterancestors()
            if a.tag in [_ns('s','Branch'),_ns('s','ForLoop'),_ns('s','QuestionModule')]
          ]):
            # This is concatenated in reverse, as the ancestors come in order from the question back to the root, and we want the opposite.

            # TODO: Below is a kludge until text components are all normalised.
            #   TextComoinents 
            if a.tag == _ns('s','QuestionModule'):
                resps = a.xpath("./s:TextComponents/s:TextComponent/s:TargetRespondent",namespaces=_namespaces)
            else:
                resps = a.xpath("./s:TextComponent/s:TargetRespondent",namespaces=_namespaces)
            text = "   "*i
            if len(resps) > 0 and resps[0].text is not None:
                text = text + resps[0].text
            else:
                text = text + "Undescribed Population"
            text = text + " (" + a.get('name') + ")"
            self.targetPopulation.addItem(text)

    def updateRefusal(self):
        newname = str(self.name.text())
        try:
            self.element.set('name',newname)
        except:
            pass
        self.update()

class Statement(SQBLNamedWidget, sqblUI.statement.Ui_Form):
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,StatementText)


class StopModule(SQBLNamedWidget, sqblUI.stopModule.Ui_Form):
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,LogicNodeText)

class CTDecisionTableHeader(QtGui.QHeaderView):
    def __init__(self, orientation, parent):
        super(CTDecisionTableHeader, self).__init__(orientation, parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.parent = parent

    def dragEnterEvent(self, event):
        # Only accept sqbl drops here
        # We may even restrict this further to only drops from the same instance
        if event.mimeData().hasFormat('text/xml+x-sqbl'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/xml+x-sqbl'):
            element = etree.fromstring(str(event.mimeData().data('text/xml+x-sqbl')))
            # We can only add questions to the table to make conditions...
            # Also, if the question is already in the table, we can't add it again.
            if self.orientation() == QtCore.Qt.Vertical and element.tag == _ns('s','Question') and element.get('name') not in self.parent.parent.questions:
                event.accept()
            # We can only add branches to the table to make conditions...
            elif self.orientation() == QtCore.Qt.Horizontal and element.tag == _ns('s','Branch'):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        element = etree.fromstring(str(event.mimeData().data('text/xml+x-sqbl')))
        if self.orientation() == QtCore.Qt.Vertical:
            self.parent.addNewQuestion.emit(element.get('name'))
        elif self.orientation() == QtCore.Qt.Horizontal:
            self.parent.addNewBranchCondition.emit(element.get('name'))

        event.setDropAction(QtCore.Qt.MoveAction)

        event.accept()

#WordSub header
class WSDecisionTableHeader(QtGui.QHeaderView):
    def __init__(self, orientation, parent):
        super(WSDecisionTableHeader, self).__init__(orientation, parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.parent = parent

    def dragEnterEvent(self, event):
        # Only accept sqbl drops here
        # We may even restrict this further to only drops from the same instance
        if event.mimeData().hasFormat('text/xml+x-sqbl'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/xml+x-sqbl'):
            element = etree.fromstring(str(event.mimeData().data('text/xml+x-sqbl')))
            # We can only add questions to the table to make conditions...
            # Also, if the question is already in the table, we can't add it again.
            if self.orientation() == QtCore.Qt.Horizontal and element.tag == _ns('s','Question') and element.get('name') not in self.parent.parent.questions:
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        element = etree.fromstring(str(event.mimeData().data('text/xml+x-sqbl')))
        if self.orientation() == QtCore.Qt.Horizontal:
            self.parent.addNewQuestion.emit(element.get('name'))
        event.setDropAction(QtCore.Qt.MoveAction)

        event.accept()


class DecisionTable(QtGui.QTableWidget):
    addNewQuestion = QtCore.pyqtSignal('QString')

    def __init__(self, rows, columns, parent):
        super(DecisionTable, self).__init__(rows, columns, parent)

        self.parent = parent 
        #self.verticalHeader().setVisible(True)
        #self.horizontalHeader().setVisible(True)

    # pos is the ordered number of the condition in the parent element
    def makeCellPair(self,pos,questionId,condition=None,value="",):
        editor = QtGui.QWidget(self)
        combo = QtGui.QComboBox(self)

        if value is None: value = ""
        index = 0
        combo.addItem("None")
        for i, x in enumerate(SQBLutil.comparisons()):
            cond,name = x
            combo.addItem(cond)
            if name == condition:
                index = i+1 
        combo.setFixedWidth(60)

        editbox = QtGui.QLineEdit(self)
        editbox.setText(value)
        editbox.setMinimumWidth(30)

        #If the index is changed to the "none" comparison, disable to value
        def changedCombo(index):
            editbox.setEnabled(index != 0)
            if index == 0: editbox.setText("") #Blank text if its None
            self.parent.cellPairComboChanged.emit(pos,index,questionId)

        def changedText():
            self.parent.cellPairTextChanged.emit(pos,questionId,editbox.text())

#        self.connect(self.model, QtCore.SIGNAL('dataChanged()'), self.thingsChanged)

        combo.setCurrentIndex(index)
        combo.currentIndexChanged.connect(changedCombo)
        editbox.editingFinished.connect(changedText)
        if index == 0:
            editbox.setEnabled(False)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(combo)
        layout.addWidget(editbox)
        layout.setSpacing(1)
        layout.setContentsMargins(1, 2, 2, 1)
        editor.setLayout(layout)
        editor.setMinimumWidth(90)
        return editor

class CTDecisionTable(DecisionTable):
    addNewBranchCondition = QtCore.pyqtSignal('QString')
    def __init__(self, rows, columns, parent):
        super(CTDecisionTable, self).__init__(rows, columns, parent)
        self.setHorizontalHeader(CTDecisionTableHeader(QtCore.Qt.Horizontal,self))
        self.setVerticalHeader(CTDecisionTableHeader(QtCore.Qt.Vertical,self))

        self.addNewQuestion.connect(self.addRow)
        self.addNewBranchCondition.connect(self.addCol)

    def addCol(self,branchName):
        # Is the branch a direct child of this object?
        # If not, error and return without doing anything.
        if len(self.parent.element.xpath(".//s:Branch[@name='%s']"%branchName,namespaces=_namespaces)) < 1:
            QtGui.QMessageBox.warning(self, 
            'Invalid Branch', 
            ".",QtGui.QMessageBox.Ok)
            return

        newCond = etree.fromstring(
            "<Condition xmlns='{s}' resultBranch='{branchName}'/>".format(
                branchName=branchName,
                s=_namespaces['s']
            )
        )
        # Add the new condition to the XML
        sg = self.parent.element.xpath(".//s:SequenceGuide",namespaces=_namespaces)[0]
        sg.append(newCond)

        # IF there is only one column and is the empty default one, delete it.
        if self.columnCount() == 1 and self.horizontalHeaderItem(0) is not None:
            self.removeColumn(0)

        #Shift otherwise branch to the end
        others = sg.xpath(".//s:Otherwise",namespaces=_namespaces)
        if len(others) > 0:
            for o in others:
                sg.append(o)

        cols = self.columnCount()

        self.insertColumn(cols)
        for row,questionID in enumerate(self.parent.questions):
            # Add the offset for the branch at the start
            editor = self.makeCellPair(cols,str(questionID))

            self.setCellWidget(row+1,cols,editor)

        # Add the branch selector
        widget = self.makeBranchSelectCell(branchName)
        self.setCellWidget(0,cols,widget)

    def addRow(self,questionID):
        # Is the question a child of this object?
        # If so, error and return without doing anything.
        if len(self.parent.element.xpath(".//s:Question[@name='%s']"%questionID,namespaces=_namespaces)) > 0:
            QtGui.QMessageBox.warning(self, 
            'Invalid Question', 
            "A condition can't be sequenced based on a question from one of its own branches.",QtGui.QMessageBox.Ok)
            return

        # We will probably want to stop people from branching on questions from after the conditional too, but thats for later.
        #    "A condition can't be sequenced based on a question that won't have been asked yet.",QtGui.QMessageBox.Ok)


        # Is the question already present
        if questionID not in self.parent.questions:
            self.parent.questions.append(questionID)
            rows = self.rowCount()
            self.insertRow(rows)
            self.setVerticalHeaderItem(rows,QtGui.QTableWidgetItem(questionID+" "))
            for col in range(0,self.columnCount()):
                editor = self.makeCellPair(col,str(questionID))

                self.setCellWidget(rows,col,editor)

    def makeBranchSelectCell(self,selected):
        combo = self.parent.makeBranchesCombo(selected=selected)
        widget = QtGui.QWidget(self)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(combo)
        layout.setContentsMargins(1, 2, 2, 1)
        widget.setLayout(layout)
        combo.setContentsMargins(1, 2, 2, 1)

        return widget


class WSDecisionTable(DecisionTable):
    def __init__(self, rows, columns, parent):
        super(WSDecisionTable, self).__init__(rows, columns, parent)
        self.setHorizontalHeader(WSDecisionTableHeader(QtCore.Qt.Horizontal,self))
        self.addNewQuestion.connect(self.addCol)

    def addRow(self):
        newCond = etree.fromstring(
            "<Condition xmlns='{s}'><ResultString/></Condition>".format(
                s=_namespaces['s']
            )
        )
        # Add the new condition to the XML
        sg = self.parent.element.append(newCond)

        row = self.rowCount()

        self.insertRow(row)
        for col,questionID in enumerate(self.parent.questions):
            editor = self.makeCellPair(row,str(questionID))
            self.setCellWidget(row,col,editor)

    def addCol(self,questionID):
        # Is the question already present
        if questionID not in self.parent.questions:
            self.parent.questions.append(questionID)
            col = self.columnCount() - 1 # offest to place before the text
            self.insertColumn(col)
            self.setHorizontalHeaderItem(col,QtGui.QTableWidgetItem(questionID+" "))
            for row in range(0,self.rowCount()):
                editor = self.makeCellPair(row,str(questionID))
                self.setCellWidget(row,col,editor)

class ConditionalTree(SQBLNamedWidget, sqblUI.conditionalTree.Ui_Form):
           #column,index of comparator, questionID, value of the edit string
    cellPairComboChanged = QtCore.pyqtSignal(int,int,'QString')
           #column, questionID, value of the edit string
    cellPairTextChanged = QtCore.pyqtSignal(int,'QString','QString')

    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,ConditionalTreeText)

        # We cache these, as a question can be in the table without actually having a condition. This cache means we can hold these non-condition questions to ensure they aren't duplicated as we add more rows in the UI.
        questions = element.xpath("./s:SequenceGuide/s:Condition/s:ValueOf/@question",namespaces=_namespaces)
        self.questions = list(set(questions))

        # Lets set up the decision table
        dt = CTDecisionTable(1,1,self)
        self.DTLayout.addWidget(dt)
        self.decisionTable = dt
        # So we can drop questions to add them

        self.updateBranchView()
        self.updateDecisionTableVert()
        self.updateDefaultBranch()
        self.addBranch.clicked.connect(self.insertBranch)
        self.deleteBranch.clicked.connect(self.removeBranch)


        self.cellPairComboChanged.connect(self.changedPairCombo)
        self.cellPairTextChanged.connect(self.changedPairText)

#        vertHeader = self.decisionTable.verticalHeader()
#        vertHeader.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#        vertHeader.customContextMenuRequested.connect(self.popupVert)

        horizHeader = self.decisionTable.horizontalHeader()
        horizHeader.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        horizHeader.customContextMenuRequested.connect(self.popupHoriz)

        self.conditionalTreeTabs.currentChanged.connect(self.setPrefTab)
        self.conditionalTreeTabs.setCurrentIndex(self.getPrefTab())
#
#    # Create pop up menu for deleting questionReferences.
#    def popupVert(self, pos):
#        header = self.codeListTable.verticalHeader()
#        menu = QtGui.QMenu()
#        deleteAction = menu.addAction("Delete Code")
#        action = menu.exec_(header.mapToGlobal(pos))
#        if action == deleteAction:
#            print "delete"

    # Create pop up menu for deleting conditionals.
    def popupHoriz(self, pos):
        header = self.decisionTable.horizontalHeader()
        menu = QtGui.QMenu()
        deleteAction = menu.addAction("Delete Condition")
        action = menu.exec_(header.mapToGlobal(pos))
        if action == deleteAction:
            col = header.visualIndex(header.logicalIndexAt(pos))
            self.decisionTable.removeColumn(col)
            condition = self.element.xpath("./s:SequenceGuide/s:Condition[position()=%s]"%(col+1),namespaces=_namespaces)[0] #Add one because XML positions are indexed from 1. DAMN IT.
            condition.getparent().remove(condition)
            self.update(big=True)
                    
        
    def changedPairCombo(self,col,index,qid):
        x = self.element.xpath("./s:SequenceGuide/s:Condition",namespaces=_namespaces)[col]
        if index > 0:
            valueof = self.getValueElement(col,qid)
            comp = SQBLutil.comparisons()[index-1][1]
            valueof.set('is',comp)
        else:
            x.remove(x.xpath("./s:ValueOf[@question='%s']"%qid,namespaces=_namespaces)[0])
            # Commenting out below as it has issues :/
            #if len(x.xpath("./s:ValueOf",namespaces=_namespaces)) == 0:
            #    x.getparent().remove(x)
        self.update()

    def changedPairText(self,col,qid,value):
        valueof = self.getValueElement(col,qid)
        valueof.text = str( value)
        self.update()

    def getValueElement(self,col,qid):
        x = self.element.xpath("./s:SequenceGuide/s:Condition",namespaces=_namespaces)[col]
        valueof = x.xpath("./s:ValueOf[@question='%s']"%qid,namespaces=_namespaces)
        if len(valueof) > 0:
            valueof = valueof[0]
        else:
            valueof = etree.Element(_ns("s","ValueOf"))
            valueof.set('question',str(qid))
            x.append(valueof)
        return valueof


    def insertBranch(self):
        newBranchName,wantToAddBranch = QtGui.QInputDialog.getText(self,
            "Enter new branch name",
            "Enter new branch name. This name needs to be unique name compared to othernames in this document.",
                )
        if wantToAddBranch:
            selected = self.model.getSelected() 
            newBranch = SQBLmodel.SQBLModuleNamedItem(etree.fromstring(SQBLmodel.newBranch(newBranchName)),selected)
            selected.addChild(newBranch)
        self.updateBranchView()
        self.update(big=True)


    def removeBranch(self):
        current = self.branchList.currentItem()

        doDelete = False
        if current is None:
            return # There is no selected branch, so just drop back out.
        name = current.text()

        numConditions = 0 #How many conditions are based on this
        numConditions = len(self.element.xpath("./s:SequenceGuide/s:Condition[@resultBranch='%s']"%name,namespaces=_namespaces))

        isDefault = False
        default = self.element.xpath("./s:SequenceGuide/s:Otherwise",namespaces=_namespaces)

        if len(default) > 0 and default[0].text == name:
            # I <3 Lazy evaluation
            isDefault = True

        if numConditions > 0 or isDefault:
            pass #confirm that we do want to delete
            
            doDelete = QtGui.QMessageBox.question(self,
                    "Removing Branch %s" % name,
                    "Removing this branch will remove the current default Branch.\n Do you want to do this?",
                    QtGui.QMessageBox.Yes,
                    QtGui.QMessageBox.No
                    ) == QtGui.QMessageBox.Yes

        if doDelete:
            self.branchList.removeItemWidget(current)
            self.model.getSelected().removeChildByName(name)
            row = self.branchList.currentRow()
            self.branchList.takeItem(row)
            if numConditions > 0:
                # remove the conditions that lead to this branch
                conditions = self.element.xpath("./s:SequenceGuide/s:Condition",namespaces=_namespaces)
                for c in conditions:
                    if c.get("resultBranch") == name:
                        c.getparent().remove(c)
            self.updateDecisionTableVert()
            if isDefault:
                default[0].getParent.remove(default[0])
            self.updateDefaultBranch()

            # Only update if we delete stuff.
            self.update(big=True)
            
    
    def getBranches(self):
        return [b for b in self.element.iterchildren(tag=_ns('s','Branch'))]

    def updateBranchView(self):
        self.branchList.clear()
        for branch in self.getBranches():
            self.branchList.addItem(branch.get('name'))

    def updateDefaultBranch(self):
        selected = None
        otherwises = self.element.xpath("./s:SequenceGuide/s:Otherwise",namespaces=_namespaces)
        if len(otherwises) > 0:
            selected = otherwises[0].get('branch')
        combo = self.makeBranchesCombo(selected=selected,
                    header = "No default, just continue",
                    existing = self.defaultBranch
                    )
        self.defaultBranch = combo 
        self.defaultBranch.currentIndexChanged.connect(self.changeDefaultBranch)

    def changeDefaultBranch(self,index):
        sg =  self.element.xpath("./s:SequenceGuide",namespaces=_namespaces)[0] #there should be only one
        otherwises = sg.xpath("./s:Otherwise",namespaces=_namespaces)
        if index == 0:
            #There is no default branch
            for o in otherwises:
                o.getparent().remove(o)
        else:
            newBranch = unicode(self.defaultBranch.itemText(index))
            if len(otherwises) > 0:
                otherwise = otherwises[0]
                # Remove any others that may be there
                for o in otherwises[1:]:
                    sg.remove(o)
            else:
                otherwise = etree.Element(_ns("s","Otherwise"))
                sg.append(otherwise)
            otherwise.set('branch',newBranch)
        self.update(big=True)


    def updateDecisionTableVert(self):
        self.decisionTable.clearContents()

        questions = set()
        for i in self.element.xpath("./s:SequenceGuide//s:ValueOf",namespaces=_namespaces):
            questions.add(i.get('question'))
        questions = list(questions)
        questions.sort()

        # Add one, cause we need the first column for Branches, this happens a few times
        self.decisionTable.setRowCount(len(questions)+1)
        # Ad
        self.decisionTable.setColumnCount(max(len(self.element.xpath("./s:SequenceGuide/s:Condition",namespaces=_namespaces)),1))
        self.decisionTable.setVerticalHeaderItem(0,QtGui.QTableWidgetItem("Branch"))
        if len(self.element.xpath("./s:SequenceGuide/s:Condition",namespaces=_namespaces)) == 0:
            self.decisionTable.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem("0"))
        for i,q in enumerate(questions):
            self.decisionTable.setVerticalHeaderItem(i+1,QtGui.QTableWidgetItem(q+" "))

        for col, rule in enumerate(self.element.xpath("./s:SequenceGuide/s:Condition",namespaces=_namespaces)):
            selected = rule.get('resultBranch')
            widget = self.decisionTable.makeBranchSelectCell(selected)

            self.decisionTable.setCellWidget(0,col,widget)
            for row,q in enumerate(questions):
                row = row + 1  #Because of the first branch column
                val = rule.xpath("./s:ValueOf[@question='%s']"%q,namespaces=_namespaces)
                if len(val)>0:
                    #There should only be one condition for this question in this set
                    text = val[0].text
                    cond = val[0].get('is')
                else:
                    # If there is no condition for this pair
                    text = ""
                    cond = None
                editor = self.decisionTable.makeCellPair(col,q,cond,text)

                self.decisionTable.setCellWidget(row,col,editor)

#            for val in rule.xpath("./s:ValueOf",namespaces=_namespaces):
#                question = val.get('question')
#                row = questions.index(question) +1 #Because of the first branch column
#                editor = self.decisionTable.makeCellPair(val.get('is'),val.text)

#                self.decisionTable.setCellWidget(row,col,editor)
        self.decisionTable.resizeColumnsToContents() 

        # Connects for allowing reordering of Branch columns conditionals
        self.decisionTable.horizontalHeader().setMovable(True)
        self.decisionTable.horizontalHeader().sectionMoved.connect(self.moveColumn)

    # Function for reordering conditionals
    # Where its stored, where it did appear, where it appears now
    def moveColumn(self,logicalIndex,oldVisIndex,newVisIndex):
        sg =  self.element.xpath("./s:SequenceGuide",namespaces=_namespaces)[0] #there should be only one
        conditions = sg.xpath("./s:Condition",namespaces=_namespaces)
        movedCondition = conditions[oldVisIndex]
        sg.insert(newVisIndex,movedCondition)
        self.update(big=True)
        

    # Accepts a text field, the id of a branch to have selected, and an existing ComboBox to be refreshed - all optional
    def makeBranchesCombo(self,header = None, selected=None,existing=None):
        if existing is not None:
            combo = existing
            combo.clear()
        else:
            combo = QtGui.QComboBox(self)

        offset = 0
        if header is not None:
            offset = 1
            header = str(header)
            combo.addItem(header)
        index = 0
        for b,branch in enumerate(self.getBranches()):
            name = branch.get('name')
            if name == selected:
                index = b + offset
            combo.addItem(branch.get('name'))
        
        combo.setCurrentIndex(index)
        return combo


#The abstract class for managing all our changes to TextComponents
class SQBLTextComponentObject(SQBLWidget):
    def __init__(self,element,model):
        SQBLWidget.__init__(self,element,model)
        self.richtextToolbars = {}

    def connect(self,UiField, tagname,richtext=False):
        # Here we catch te textChanged SIG from QTextEdit and QLineEdit
        # QLineEdit gives the text as well, but just catch it and throw it away.

        if richtext: 
            def canInsertFromMimeData(q,s=UiField): 
                if q.hasFormat("text/xml+x-sqbl+wordsub"):
                    return True
                else:
                    QtGui.QTextEdit.canInsertFromMimeData(s,q) 
            UiField.canInsertFromMimeData = canInsertFromMimeData

            def insertFromMimeData(q,s=UiField): 
                if q.hasFormat("text/xml+x-sqbl+wordsub"):
                    insert = str(q.data('text/xml+x-sqbl+wordsub'))
                    s.insertPlainText(insert)
                else:
                    QtGui.QTextEdit.insertFromMimeData(s,q) 
            UiField.insertFromMimeData = insertFromMimeData
            # Assign highlighter below as its destroyed in Python x86 32bit.
            # See: http://qt-project.org/forums/viewthread/26371
            self.highlighter = SQBLutil.XMLHighlighter(UiField.document())
        
        def updateTagName(str=None):
            elem = self.element.xpath("./s:%s" % tagname,namespaces=_namespaces)
            if len(elem) > 0:
                elem = elem[0]
            else:
               
                elem = etree.Element(_ns("s",tagname))
                self.element.append(elem)
            
            #For now, richtext is "too hard"
            if not richtext:
                try:
                    # Is this a QLineEdit?
                    elem.text = unicode(UiField.text())
                except AttributeError:
                    # Or a plain text QTextEdit
                    elem.text = unicode(UiField.toPlainText())
                except:
                    # Oh, it isn't well, better fail then.
                    raise 
            else:
                pos = UiField.cursorRect(UiField.textCursor()).topLeft()
                pos = UiField.mapToGlobal(pos)
                try:
                    root = etree.fromstring("<x xmlns='sqbl:1'>"+unicode(UiField.toPlainText())+"</x>")
                    QtGui.QToolTip.hideText()
                    elem.text = root.text
                    for e in elem:
                        elem.remove(e)
                    for e in root:
                        elem.append(e)

                except etree.XMLSyntaxError, e:
                    msg = e.error_log.last_error.message
                    line=e.error_log.last_error.line
                    col=e.error_log.last_error.column
                    ttText = "Invalid XML: Line %s, Col %s\n %s"%(line,col,msg)
                    QtGui.QToolTip.showText(pos,ttText)
                    elem.text = unicode(UiField.toPlainText())
                    for e in elem:
                        elem.remove(e)
                except:
                    QtGui.QToolTip.showText(pos,"Invalid XML: Unknown error")
                    raise
            self.update()

        text = ""
        elem = self.element.xpath("./s:%s" % tagname,namespaces=_namespaces)
        if richtext and len(elem) > 0:
            text = SQBLutil.getRichTextAsMarkup(elem[0])
            UiField.insertPlainText(text)
            index = self.verticalLayout.indexOf(UiField)
            self.richtextToolbars[tagname] = RichTextToolBar()
            self.verticalLayout.insertWidget(index,self.richtextToolbars[tagname])
            self.verticalLayout.update()
        else:
            if len(elem) > 0:
                text = SQBLutil.getRichTextAsMarkup(elem[0])
            if text is None:
                text = ""
            UiField.setText(text)

        try:
            UiField.editingFinished.connect(updateTagName)
        except:
            # Override focusout to throw an editing finished signal.
            def focusOutEvent(event):
                QtGui.QTextEdit.focusOutEvent(UiField,event)
                UiField.emit(QtCore.SIGNAL("editingFinished()"))
            UiField.focusOutEvent = focusOutEvent
            UiField.connect(UiField, QtCore.SIGNAL('editingFinished()'), updateTagName)
            UiField.textChanged.connect(updateTagName)

class QuestionModuleText(SQBLTextComponentObject, sqblUI.questionModuleText.Ui_Form):
    def __init__(self,element,model):
        SQBLTextComponentObject.__init__(self,element,model)
        self.connect(self.longName,"LongName")
        self.connect(self.title,"Title")
        self.connect(self.purpose,"Purpose")
        self.connect(self.targetRespondent,"TargetRespondent")

class QuestionText(SQBLTextComponentObject, sqblUI.questionText.Ui_Form):
    def __init__(self,element,model):
        SQBLTextComponentObject.__init__(self,element,model)
        self.connect(self.questionText,"QuestionText",richtext=True)
        self.connect(self.questionIntent,"QuestionIntent")
        self.connect(self.instruction,"Instruction",richtext=True)

class ConditionalTreeText(SQBLTextComponentObject, sqblUI.conditionalTreeText.Ui_Form):
    def __init__(self,element,model):
        SQBLTextComponentObject.__init__(self,element,model)
        self.connect(self.instruction,"Instruction",richtext=True)
        self.connect(self.purpose,"Purpose")

class StatementText(SQBLTextComponentObject, sqblUI.statementText.Ui_Form):
    def __init__(self,element,model):
        SQBLTextComponentObject.__init__(self,element,model)
        self.connect(self.statementText,"StatementText",richtext=True)

# Reusable by widgets for all 'NogicNodes', eg. Conditionals, Loops, etc...
class LogicNodeText(SQBLTextComponentObject, sqblUI.logicNodeText.Ui_Form):
    def __init__(self,element,model):
        SQBLTextComponentObject.__init__(self,element,model)
        self.connect(self.instruction,"Instruction",richtext=True)
        self.connect(self.purpose,"Purpose")
        self.connect(self.targetRespondent,"TargetRespondent")

class RichTextToolBar(QtGui.QWidget):
     def __init__(self):
        QtGui.QWidget.__init__(self)
        self.frame = QtGui.QFrame()
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)

        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)

        self.textBold = QtGui.QPushButton(self.frame)
        self.textBold.setMaximumSize(QtCore.QSize(25, 25))
        self.textBold.setCheckable(True)
        self.textBold.setText("B")
        self.horizontalLayout.addWidget(self.textBold)
        
        self.textItalic = QtGui.QPushButton(self.frame)
        self.textItalic.setMaximumSize(QtCore.QSize(25, 25))
        self.textItalic.setCheckable(True)
        self.textItalic.setText("I")
        self.horizontalLayout.addWidget(self.textItalic)
        
        self.textUnderline = QtGui.QPushButton(self.frame)
        self.textUnderline.setMaximumSize(QtCore.QSize(25, 25))
        self.textUnderline.setCheckable(True)
        self.textUnderline.setText("U")
        self.horizontalLayout.addWidget(self.textUnderline)
        
        self.fontComboBox = QtGui.QFontComboBox(self.frame)
        self.horizontalLayout.addWidget(self.fontComboBox)

class WordSub(SQBLNamedWidget, sqblUI.wordSub.Ui_Form):
    #Signal fired if the combo box for a comparator in a pair is changed
    #column,index of comparator, questionID, value of the edit string
    cellPairComboChanged = QtCore.pyqtSignal(int,int,'QString')
    #Signal fired if the text box for a value in a pair is changed
    #column, questionID, value of the edit string
    cellPairTextChanged = QtCore.pyqtSignal(int,'QString','QString')
    def __init__(self,element,model):
        SQBLNamedWidget.__init__(self,element,model,WordSubText)

        dt = WSDecisionTable(0,0,self)
        self.DTLayout.addWidget(dt)
        self.decisionTable = dt

        self.updateDecisionTable()
        self.languagePicker.languageList.currentIndexChanged[int].connect(self.changeDecisionTableLanguage)
        self.decisionTable.itemChanged.connect(self.updateResultText)
        questions = element.xpath("./s:Condition/s:ValueOf/@question",namespaces=_namespaces)
        self.questions = list(set(questions))
        self.decisionTable.addNewQuestion.connect(self.enableConditionButtons)
        self.addCondition.clicked.connect(self.decisionTable.addRow)
        if len(self.questions) == 0:
            self.disableConditionButtons()
        else:
            self.updateConditionButtons()

    def enableConditionButtons(self): self.updateConditionButtons(True)
    def disableConditionButtons(self): self.updateConditionButtons(False)
    def updateConditionButtons(self,enabled=True):
        self.addCondition.setEnabled(enabled)
        self.removeCondition.setEnabled(enabled)

    def updateTagName(self,text):
        lang = self.languages.itemData(self.languages.currentIndex()).toPyObject()
        elem = self.element.xpath("./s:ResultString" % (tagname),namespaces=_namespaces)[0]
        self.updateTextComponent(lang,text,elem)

    def updateResultText(self,item):
        if item is None:
            #How did you get here ?
            return
        if item.column()+1 != self.decisionTable.columnCount():
            #These changes get picked up elsewhere.
            return
        langPicker = self.languagePicker.languageList
        lang = str(langPicker.itemData(langPicker.currentIndex()).toPyObject())
        text = self.element.xpath("./s:Condition[%d]/s:ResultString/s:TextComponent[@xml:lang='%s']" % (item.row()+1,lang),namespaces=_namespaces) # Add one because XML :(
        value = unicode(item.text())
        if len(text) > 0:
            text[0].text = value
        else:
            #There is no text yet...
            elem = self.element.xpath("./s:Condition[%d]/s:ResultString" % (item.row()+1),namespaces=_namespaces)[0] # Add one because XML :(
            element = etree.Element("{%s}TextComponent"%(_namespaces['s']))
            element.set("{%s}lang"%(_namespaces['xml']),lang)
            element.text = value
            elem.append(element)
        self.update()

    # This function updates the value of this text box if the language picker changes
    def changeDecisionTableLanguage(self,index):
        langPicker = self.languagePicker.languageList
        lang = str(langPicker.itemData(index).toPyObject())
        for row, rule in enumerate(self.element.xpath("./s:Condition",namespaces=_namespaces)):
            selected = rule.xpath("./s:ResultString/s:TextComponent[@xml:lang='%s']" % (lang),namespaces=_namespaces)
            if len(selected) > 0:
                text = selected[0].text
            else:
                text = ""
            widget = QtGui.QTableWidgetItem(text)
            col = self.decisionTable.columnCount() - 1
            self.decisionTable.setItem(row,col,widget)

    def updateDecisionTable(self):
        self.decisionTable.clearContents()

        questions = set()
        for i in self.element.xpath(".//s:ValueOf",namespaces=_namespaces):
            questions.add(i.get('question'))
        questions = list(questions)
        questions.sort()

        langPicker = self.languagePicker.languageList
        lang = str(langPicker.itemData(langPicker.currentIndex()).toPyObject())

        # Add one, cause we need the first column for Branches, this happens a few times
        self.decisionTable.setColumnCount(len(questions)+1) # Add one for text column
        self.decisionTable.setRowCount(len(self.element.xpath("./s:Condition",namespaces=_namespaces)))
        if len(self.element.xpath("./s:Condition",namespaces=_namespaces)) == 0:
            self.decisionTable.setVerticalHeaderItem(0,QtGui.QTableWidgetItem("0"))
        for i,q in enumerate(questions):
            self.decisionTable.setHorizontalHeaderItem(i,QtGui.QTableWidgetItem(q+" "))

        col=-1 # we use this later. If ther are no conditions, this gets incremented to one
        for row, rule in enumerate(self.element.xpath("./s:Condition",namespaces=_namespaces)):
            for col,q in enumerate(questions):
                val = rule.xpath("./s:ValueOf[@question='%s']"%q,namespaces=_namespaces)
                if len(val)>0:
                    #There should only be one condition for this question in this set
                    text = val[0].text
                    cond = val[0].get('is')
                else:
                    # If there is no condition for this pair
                    text = ""
                    cond = None
                editor = self.decisionTable.makeCellPair(row,q,cond,text)

                self.decisionTable.setCellWidget(row,col,editor)
                #self.decisionTable.setItem(row,col,editor)

            selected = rule.xpath("./s:ResultString/s:TextComponent[@xml:lang='%s']" % (lang),namespaces=_namespaces)
            if len(selected) > 0:
                text = selected[0].text
            else:
                text = ""
            widget = QtGui.QTableWidgetItem(text)
            self.decisionTable.setItem(row,col+1,widget)

        self.decisionTable.setHorizontalHeaderItem(col+1,QtGui.QTableWidgetItem("Text"))
        self.decisionTable.resizeColumnsToContents() 
        self.decisionTable.horizontalHeader().setStretchLastSection(True)

        self.cellPairComboChanged.connect(self.changedPairCombo)
        self.cellPairTextChanged.connect(self.changedPairText)

        # Connects for allowing reordering of Branch columns conditionals
        self.decisionTable.verticalHeader().setMovable(True)
        #self.decisionTable.verticalHeader().sectionMoved.connect(self.moveRow)

    def changedPairCombo(self,col,index,qid):
        x = self.element.xpath("./s:Condition",namespaces=_namespaces)[col]
        if index > 0:
            valueof = self.getValueElement(col,qid)
            comp = SQBLutil.comparisons()[index-1][1]
            valueof.set('is',comp)
        else:
            x.remove(x.xpath("./s:ValueOf[@question='%s']"%qid,namespaces=_namespaces)[0])
            # Commenting out below as it has issues :/
            # TODO: Deleting the condition SHOULD be fine, but it means columns and conditions get out of sync, causing buggy behaviour. Fix this in the other place too.
            #if len(x.xpath("./s:ValueOf",namespaces=_namespaces)) == 0:
            #    x.getparent().remove(x)
        self.update()

    def changedPairText(self,col,qid,value):
        valueof = self.getValueElement(col,qid)
        valueof.text = str(value)
        self.update()

    def getValueElement(self,col,qid):
        x = self.element.xpath("./s:Condition",namespaces=_namespaces)[col]
        valueof = x.xpath("./s:ValueOf[@question='%s']"%qid,namespaces=_namespaces)
        if len(valueof) > 0:
            valueof = valueof[0]
        else:
            valueof = etree.Element(_ns("s","ValueOf"))
            valueof.set('question',str(qid))
            x.insert(0,valueof)
        return valueof

class WordSubText(SQBLTextComponentObject, sqblUI.wordSubText.Ui_Form):
    def __init__(self,element,model):
        SQBLTextComponentObject.__init__(self,element,model)
        self.connect(self.intentText,"Intent")
        self.connect(self.defaultText,"Default")
        self.connect(self.staticText,"Static")

