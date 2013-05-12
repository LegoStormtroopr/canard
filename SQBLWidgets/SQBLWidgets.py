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
        print index,rows
        for row in rows:
            self.subQuestionList.removeRow(row)
            subQ = self.subQuestions.xpath("s:SubQuestion",namespaces=_namespaces)[row] 
            print etree.tostring(subQ)
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
        self.subQuestionList.clear()
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

        responseTypes = ["Text","Number", "Code list"]
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
        print "hello",tabFrom,tabTo
        movedResponse = self.responses.xpath("./*",namespaces=_namespaces)[tabFrom]
        self.responses.insert(tabTo,movedResponse)
        self.update()


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
        addNum = arbMenu.addAction("Numeric Response")
        addText = arbMenu.addAction("Text Response")
        addCode = arbMenu.addAction("CodeList Response")
        
        addNum.triggered.connect(self.addNumericResponse)
        addText.triggered.connect(self.addTextResponse)
        addCode.triggered.connect(self.addCodeListResponse)
        arb.setMenu(arbMenu)

        self.responseTabs.setCornerWidget(arb)
        for response in self.responses:
            responseField = None
            if response.tag == _ns("s","CodeList"):
                responseField = Responses.CodeList(response,self.model) 
                #self.responseType.setCurrentIndex(2)
                tabName = "Codelist"
            elif response.tag == _ns("s","Number"):
                responseField = Responses.Number(response,self.model) 
                #self.responseType.setCurrentIndex(1)
                tabName = "Number"
            elif response.tag == _ns("s","Text"):
                responseField = Responses.Text(response,self.model) 
                #self.responseType.setCurrentIndex(0)
                tabName = "Text"
            if responseField is not None:
                self.responseTabs.addTab(responseField,tabName)
        self.responseTabs.tabCloseRequested.connect(self.removeResponse)

    def removeResponse(self,index):
        self.responses.remove(self.responseTabs.widget(index).element)
        self.responseTabs.removeTab(index)
        self.update()

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
            print values

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
            resps = a.xpath("./s:TextComponent/s:TargetRespondent",namespaces=_namespaces)
            text = "   "*i
            if len(resps) > 0:
                text = text + resps[0].text
            else:
                text = text + "Undescribed population"
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

class DecisionTableHeader(QtGui.QHeaderView):
    def __init__(self, orientation, parent):
        super(DecisionTableHeader, self).__init__(orientation, parent)
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


class DecisionTable(QtGui.QTableWidget):
    addNewQuestion = QtCore.pyqtSignal('QString')
    addNewBranchCondition = QtCore.pyqtSignal('QString')

    def __init__(self, rows, columns, parent):
        super(DecisionTable, self).__init__(rows, columns, parent)
        self.setHorizontalHeader(DecisionTableHeader(QtCore.Qt.Horizontal,self))
        self.setVerticalHeader(DecisionTableHeader(QtCore.Qt.Vertical,self))

        self.addNewQuestion.connect(self.addRow)
        self.addNewBranchCondition.connect(self.addCol)
        self.parent = parent 
        self.verticalHeader().setVisible(True)
        self.horizontalHeader().setVisible(True)

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
            editor = self.makeCellPair(row,cols,str(questionID))

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
                editor = self.makeCellPair(rows,col,str(questionID))

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

    def makeCellPair(self,row,col,questionId,condition=None,value="",):
        editor = QtGui.QWidget(self)
        combo = QtGui.QComboBox(self)

        index = 0
        combo.addItem("None")
        for i, x in enumerate(SQBLutil.comparisons()):
            cond,name = x
            combo.addItem(cond)
            if name == condition:
                index = i+1 
        combo.setFixedWidth(60)
        combo.setStyleSheet('font-size: 11pt;')

        editbox = QtGui.QLineEdit(self)
        editbox.setText(value)
        editbox.setMaximumWidth(100)

        #If the index is changed to the "none" comparison, disable to value
        def changedCombo(index):
            editbox.setEnabled(index != 0)
            editbox.setText("")
            self.parent.cellPairComboChanged.emit(col,index,questionId)

        def changedText():
            self.parent.cellPairTextChanged.emit(col,questionId,editbox.text())
            print col,questionId,editbox.text()

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
        dt = DecisionTable(1,1,self)
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
            print "delete"
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
            if len(x.xpath("./s:ValueOf",namespaces=_namespaces)) == 0:
                x.getparent().remove(x)
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
        print [self.defaultBranch.itemText(i) for i in range(self.defaultBranch.count())]
        print self.defaultBranch.isEnabled()

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
                editor = self.decisionTable.makeCellPair(row,col,q,cond,text)

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
        

## All below is out of sync with the vert and needs a big update to be ready.
## HOWEVER, it seems like a horiontal view of the decision table would be un user-friendly.
##    def updateDecisionTableHoriz(self):
##        self.decisionTable.clearContents()
##        self.decisionTable.setRowCount(1)
##
##        questions = set()
##        for i in self.element.xpath("./s:SequenceGuide//s:ValueOf",namespaces=_namespaces):
##            questions.add(i.get('question'))
##        questions = list(questions)
##        questions.sort()
##
##        # Add one, cause we need the first column for Branches, this happens a few times
##        self.decisionTable.setColumnCount(len(questions)+1)
##        self.decisionTable.setHorizontalHeaderItem(0,QtGui.QTableWidgetItem("Branch"))
##        for i,q in enumerate(questions):
##            self.decisionTable.setHorizontalHeaderItem(i+1,QtGui.QTableWidgetItem(q))
##
##        for row, cond in enumerate(self.element.xpath("./s:SequenceGuide/s:Condition",namespaces=_namespaces)):
##            selected = cond.get('resultBranch')
##            combo = self.makeBranchesCombo(selected=selected)
##            widget = QtGui.QWidget(self)
##            layout = QtGui.QHBoxLayout(self)
##            layout.addWidget(combo)
##            layout.setContentsMargins(1, 2, 2, 1)
##            widget.setLayout(layout)
##
##            combo.setContentsMargins(1, 2, 2, 1)
##
##            self.decisionTable.setCellWidget(row,0,widget)
##            for val in cond.xpath("./s:ValueOf",namespaces=_namespaces):
##                question = val.get('question')
##                col = questions.index(question) +1 #Because of the first branch column
##                editor = self.decisionTable.makeCellPair(val.get('is'),val.text)
##
##                self.decisionTable.setCellWidget(row,col,editor)
##        self.decisionTable.resizeColumnsToContents() 

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
        def updateTagName(str=None):
            elem = self.element.xpath("./s:%s" % tagname,namespaces=_namespaces)
            if len(elem) > 0:
                elem = elem[0]
            else:
               
                elem = etree.Element(_ns("s",tagname))
                self.element.append(elem)

            #For now, richtext is "too hard"
            if not richtext or True:
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
                rt = unicode(UiField.toHtml())
                rt.replace('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">',"")
                xml = etree.fromstring(rt)
                elem.clear()
                for p in xml.xpath("//body/p"):
                    p.attrib.pop('style')
                    elem.append(p)
                #elem.text = str(UiField.toHtml())
            self.update()

        text = ""
        elem = self.element.xpath("./s:%s" % tagname,namespaces=_namespaces)
        if richtext and len(elem) > 0:
            text = elem[0].text
            if text is None:
                text = ""
            for i in elem[0].iterchildren():
                text = text + etree.tostring(i)
            UiField.insertHtml(text)
            index = self.verticalLayout.indexOf(UiField)
            self.richtextToolbars[tagname] = RichTextToolBar()
            self.verticalLayout.insertWidget(index,self.richtextToolbars[tagname])
            self.verticalLayout.update()
        else:
            if len(elem) > 0:
                text = elem[0].text
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
        self.connect(self.statementText,"StatementText")

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

