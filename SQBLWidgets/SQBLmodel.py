from PyQt4 import QtCore, QtGui, QtWebKit
from lxml import etree
from lxml import objectify

_namespaces = {
    "s"  : "sqbl:1",
    "q"  : "qwac:reusable:1",
    "t"  : "tusl:1",
    "xml": "http://www.w3.org/XML/1998/namespace",
}
def _ns(prefix,tag):
    return("{%s}%s"%(_namespaces[prefix],tag))

class QuestionModule(QtCore.QAbstractItemModel):  
    def __init__(self, xml, parent=None):  
        super(QuestionModule, self).__init__(parent)  
        self.parents=[]  

        parser = etree.XMLParser(encoding='utf-8')
                
        self.sqbl = objectify.fromstring(xml,parser=parser)
        self.aboutToMove = None # Indexes we are about to move

        self.rootItem = TreeItem([u"NameOfColumn"])  
        self.setupModelData(self.sqbl, self.rootItem)  

        self.icons = {
                _ns('s',"Statement"): QtGui.QIcon("icons/Statement.png"),
                _ns('s',"ConditionalTree"): QtGui.QIcon("icons/ConditionalTree.png"),
                _ns('s',"Question"):  QtGui.QIcon("icons/Question.png"),
                _ns('s',"ForLoop"):  QtGui.QIcon("icons/Loop.png"),
                _ns('s',"ModuleExitPoint"):  QtGui.QIcon("icons/StopModule.png"),
                _ns('s',"QuestionGroup"):  QtGui.QIcon("icons/QuestionGroup.png"),
                _ns('s',"Branch"):  QtGui.QIcon("icons/Branch.png"),
                _ns('s',"WordSub"):  QtGui.QIcon("icons/WordSub.png"),
                }
    def setSelected(self,selected):
        self.selected = selected

    def getSelected(self):
        return self.selected

    def getXMLstring(self):
        return etree.tostring(self.sqbl)
    def getXMLetree(self):
        return self.sqbl
    
    def isUniqueName(self,name):
        elems = self.sqbl.xpath("//*[@name='%s']"%name)
        return len(elems) <= 1 #If there are zero element with this name it is also unique

    def getModuleName(self,lang='en'):
        names = self.sqbl.xpath("/s:QuestionModule/s:TextComponent[@xml:lang='%s']/s:LongName"%lang,namespaces=_namespaces)
        
        if len(names) > 0:
            return str(names[0].text)
        
        return "Untitled Module"

    def setupModelData(self,data,parent):
        module = SQBLModuleNamedItem(data,parent,
                icon=QtGui.QIcon("icons/Module.png")
                )
        parent.appendChild(module)

        pop = data.xpath('./s:IncomingPopulation',namespaces=_namespaces)
        if len(pop) == 0:
            pop = etree.Element("{%s}IncomingPopulation"%(_namespaces['s']))
            # Need to re-think this part, it was rushed.
            # We won't insert it yet
            # data.insert(0,pop)
        else:
            pop = pop[0]
        populations = SQBLModuleUnnamedItem(
                pop,
                module,
                label=u"Incoming Populations",
                icon=QtGui.QIcon("icons/Populations.png")
                )
        module.appendChild(populations)

        ws = data.xpath('./s:WordSubstitutions',namespaces=_namespaces)
        if len(ws) == 0:
            ws = etree.Element("{%s}WordSubstitutions"%(_namespaces['s']))
            # Need to re-think this part, it was rushed.
            # We won't insert it yet
            # data.insert(0,pop)
        else:
            ws = ws[0]

        wordSubs = SQBLModuleUnnamedItem(
                ws,
                module,
                label=u"Word Substitutions",
                icon=QtGui.QIcon("icons/Populations.png")
                )
        module.appendChild(wordSubs)
        for sub in ws.iterchildren(tag=_ns('s','WordSub')):
            wordSubs.appendChild(SQBLModuleNamedItem(sub,wordSubs))

        modLogic = [i for i in data.iterchildren(tag=_ns('s','ModuleLogic'))][0]
        logic = SQBLModuleUnnamedItem(
                modLogic,module,label=u"Flow Logic",
                icon=QtGui.QIcon("icons/ModuleLogic.png")
                )
        module.appendChild(logic)

        for element in modLogic:
            if element.tag not in [etree.Comment, etree.PI]:
                logic.appendChild(SQBLModuleNamedItem(element,logic))
        module.expanded =  True

        di = data.xpath('./s:DerivedDataItems',namespaces=_namespaces)
        if len(di) == 0:
            di = etree.Element("{%s}DerivedDataItems"%(_namespaces['s']))
            # Need to re-think this part, it was rushed.
            # We won't insert it yet
            #data.insert(0,di)
        else:
            di = di[0]
        derivedDI = SQBLModuleUnnamedItem(di,module,
                label=u"Derived Data Items",
                icon=QtGui.QIcon("icons/Derived.png")
                )
        module.appendChild(derivedDI)

        sm = data.xpath('./s:Submodules',namespaces=_namespaces)
        if len(sm) == 0:
            sm = etree.Element("{%s}Submodules"%(_namespaces['s']))
            # Need to re-think this part, it was rushed.
            # We won't insert it yet
            # data.insert(0,sm)
        else:
            sm = sm[0]
        submodules = SQBLModuleUnnamedItem(sm,module,
                label=u"SubModules",
                icon=QtGui.QIcon("icons/SubModules.png")
                )
        module.appendChild(submodules)

  #Element is XML object
  #parent is TreeItem
    def setupLogic(self,element,parent):
        # We may return to the "unanmed items in the future.
        #if element.tag == _ns('s','Statement'):
        #    newparent = SQBLModuleUnnamedItem(element,parent) 
        #else:
        
        return newparent

    def deleteSelected(self):
#        self.selected.internalPointer.parent().removeChildByName( 
        pass

    def removeChildByName(self,childName,parent=None):
        if parent is None:
            parent=self.selected.internalPointer()
        parent.removeChildByName(childName)
        self.emit(QtCore.SIGNAL('layoutChanged()'))

    def data(self, index, role):  
        if not index.isValid():  
            return None  
        item = index.internalPointer() 
        if role == QtCore.Qt.DecorationRole:
            icon = item.getIcon()
            if icon is not None:
                return icon
            else:
                return self.icons.get(item.element.tag,None)
#        if role == QtCore.Qt.SizeHintRole:
#            size=item.iconSize
#            return QtCore.QSize(size,size)
        if role == QtCore.Qt.DisplayRole:  
            return QtCore.QVariant(item.data(index.column()))  
        if role == "element":
            return index.internalPointer().getElement()

        return None  
    
    def setData(self, index, value, role):  
         if index.isValid() and role == QtCore.Qt.EditRole:  
   
             prev_value = self.getValue(index)  
   
             item = index.internalPointer()  
   
             item.setData(unicode(value.toString()))  
   
             return True  
         else:  
             return False  

    def flags(self, index):  
        if not index.isValid():  
            return QtCore.Qt.NoItemFlags  

        actions =  QtCore.Qt.ItemIsEnabled |\
                   QtCore.Qt.ItemIsSelectable |\
                   QtCore.Qt.ItemIsEditable

        item = index.internalPointer()
        if item.canDrag():
            actions = actions | QtCore.Qt.ItemIsDragEnabled
        if item.canDrop():
            actions = actions | QtCore.Qt.ItemIsDropEnabled

        return actions

    def supportedDragActions(self): 
        return QtCore.Qt.MoveAction
    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction         
        return QtCore.Qt.MoveAction

    def mimeTypes(self):
        return ['text/xml+x-sqbl','text/xml+x-sqbl+new']

    def mimeData(self, indexes):
        self.aboutToMove = indexes # set the indexes we are about to move, so we can use them on the drop
        # Only one thing can be selected, so we can just grab the first one, and serialise its XML
        data = indexes[0].internalPointer().getXML()
        mimedata = QtCore.QMimeData()
        mimedata.setData('text/xml+x-sqbl', data)
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):

        parent = parent.internalPointer()
        element = etree.fromstring(str(data.data('text/xml+x-sqbl')))
        if parent.canDrop():
            if data.hasFormat("text/xml+x-sqbl+new"):
                self.aboutToMove = None
            if element.tag == _ns("s","Branch"):
                # We can't just drop branches anywhere!
                return False
            if parent.element.tag == _ns("s","QuestionGroup") and \
                    element.tag != _ns("s","Question"):
                return False
            if self.aboutToMove is not None:
                # If we are about to move something internally, and its a move operation:
                #  get the child object to move and remove it from its parent
                child = self.aboutToMove[0].internalPointer()
                child.parentItem.childItems.remove(child) 
            elif data.data('text/xml+x-sqbl') is not None:
                
                child = SQBLModuleNamedItem(element,parent)
                
            #True is here as we haven't implemented when youa re allowed to drop on some stuff"
            if True or child.isLogicBlock and parent.isLogicHead:
                parent.addChild(child,row)
                self.emit(QtCore.SIGNAL('layoutChanged()'))

            self.aboutToMove = None
            return True
        else:
            return False

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/xml+x-sqbl'):
            event.accept()


#EVERYTHING BELOW HERE IS COPY/PASTED YOU NEED TO UNDERSTAND THIS!!!
     
    def nodeFromIndex(self, index):  
           if index.isValid():  
               return index.internalPointer()  
           else:  
               return self.rootItem  
     
    def getValue(self, index):  
           item = index.internalPointer()  
           return item.data(index.column())  
     
    def columnCount(self, parent):  
           if parent.isValid():  
               return parent.internalPointer().columnCount()  
           else:  
               return self.rootItem.columnCount()  
     

    def headerData(self, section, orientation, role):  
           if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:  
               return QtCore.QVariant(self.rootItem.data(section)[0])  
     
           return None  
     
    def index(self, row, column, parent):  
     
           if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):  
               return QtCore.QModelIndex()  
     
           if not parent.isValid():  
               parentItem = self.rootItem  
           else:  
               parentItem = parent.internalPointer()  
     
           childItem = parentItem.child(row)  
           if childItem:  
               return self.createIndex(row, column, childItem)  
           else:  
               return QtCore.QModelIndex()  
     
    def parent(self, index):  
           if not index.isValid():  
               return QtCore.QModelIndex()  
     
           childItem = index.internalPointer()  
           parentItem = childItem.parent()  
     
           if parentItem == self.rootItem:  
               return QtCore.QModelIndex()  
     
           return self.createIndex(parentItem.row(), 0, parentItem)  
     
    def rowCount(self, parent):  
           if parent.column() > 0:  
               return 0  
     
           if not parent.isValid():  
               parentItem = self.rootItem  
           else:  
               parentItem = parent.internalPointer()  
    
           return parentItem.childCount()  

    # finds all questions prior to the endpoint
    # Returns the name and question text in the given language as a list of tuples.
    def findQuestions(self,lang,endpoint=None):
        if endpoint is None:
            questions = self.sqbl.xpath(".//s:Question",namespaces=_namespaces)
            texts = [] 
            for q in questions:
                name = q.get("name")
                text = etree.tostring(q.xpath("./s:TextComponent[@xml:lang='%s']/s:QuestionText"%(lang),namespaces=_namespaces)[0], method="text")
                if text is None:
                    text = "No question text"
                else:
                    #Strip and normalise all white space, just for display
                    import re
                    text = text.strip()
                    text = re.sub(r'\s+', ' ', text)

                texts.append((name,text))
            return texts
        else:
            print "fail"





class TreeItem(object):  
      def __init__(self, data, parent=None,drop=False,icon=None,iconSize=0):  
          self.parentItem = parent  
          self.itemData = data  
          self.childItems = []  
          self.drop=False
          self.icon=icon
          self.iconSize=iconSize

      def getIcon(self):
          return self.icon
    
      def appendChild(self, item):  
          self.childItems.append(item)  
    
      def removeChild(self,item):
          self.childItems.pop(self.childItems.index(item))

      def child(self, row):  
          return self.childItems[row]  
    
      def childCount(self):  
          return len(self.childItems)  
    
      def columnCount(self):  
          return len(self.itemData)  
    
      def data(self, column):  
          try:  
              return self.itemData  
   
          except IndexError:  
              return None  
    
      def parent(self):  
          return self.parentItem  
    
      def row(self):  
          if self.parentItem:  
              return self.parentItem.childItems.index(self)  
    
          return 0  
      def setData(self, data):  
          self.itemData = data

      def canDrop(self):
          return self.drop
      def canDrag(self):
          return False
      def getElement(self):  
          return None

class SQBLModuleTreeItem(TreeItem):  

    def __init__(self, data, parent=None,icon=None,iconSize=0):  
        self.parentItem = parent  
        self.childItems = []  
        self.icon=icon
        self.iconSize=iconSize
        self.element = data

    def getIcon(self):
        return self.icon

    def getElement(self):
        return self.element
  
    def data(self,column):
        return self.itemData

    def setData(self, data):
        self.itemData = data

    def move(self,newparent):
        self.parentItem.removeChild(self)
        self.parentItem = newparent
        self.parentItem.addChild(self,move=True)

    def getXML(self):
        return etree.tostring(self.element)
                
    def canDrop(self):
        #Most SQBL things can't be dropped on, so define those that can
        if self.element.tag in (
               _ns("s","Branch"),
               _ns("s","ModuleLogic"),
               _ns("s","QuestionGroup"),
           ):
            return True
        return False
    def canDrag(self):
        #Most SQBL things can be dragged, so define those that can't
        if self.element.tag in (
               #_ns("s","Branch"), These are draggable to make decision tables
               _ns("s","ModuleLogic"),
           ):
            return False
        return True

    def addChild(self, child,position=-1):  
        child.parentItem = self
        dropSpot = self.element
        if self.element.tag == _ns("s","Branch"):
            # We actually need to put the item in the BranchLogic element just under here.
            # There is only, so just take the first
            dropSpot = self.element.xpath("./s:BranchLogic",namespaces=_namespaces)[0]
        elif self.element.tag == _ns("s","QuestionGroup"):
            # We actually need to put the item in the BranchLogic element just under here.
            # There is only, so just take the first
            dropSpot = self.element.xpath("./s:GroupedQuestions",namespaces=_namespaces)[0]
        if position == -1:
            self.childItems.append(child)
            dropSpot.append(child.element)
        else:
            self.childItems.insert(position,child) 
            dropSpot.insert(position,child.element)

    def removeChild(self,child):
        if self.element.tag == _ns('s','Branch'):
            self.element.xpath("./s:BranchLogic",namespaces=_namespaces)[0].remove(child.element)
        else:
           self.element.remove(child.element)
        super(SQBLModuleTreeItem,self).removeChild(child)

    def removeChildByName(self,name):
        elems = self.element.xpath("*[@name='%s']"%name)
        if len(elems) > 0:
            child = [ c for c in self.childItems if c.itemData == name][0]
            self.removeChild(child)

class SQBLModuleUnnamedItem(SQBLModuleTreeItem):
    def __init__(self, data, parent=None,label=None,icon=None,iconSize=0):  
        SQBLModuleTreeItem.__init__(self,data,parent,icon,iconSize)
        if label is not None:
            self.setData(label)
        else:
            self.setData(self.element.tag)

class SQBLModuleNamedItem(SQBLModuleTreeItem):  
    def __init__(self, data, parent=None,icon=None,iconSize=0):  
        SQBLModuleTreeItem.__init__(self,data,parent,icon,iconSize)

        self.setData(self.element.get('name'))
        self.setupLogic()

    # Recursively build out model down the tree
    def setupLogic(self):
        if self.element.tag == _ns('s','ConditionalTree'):
            for branch in self.element.iterchildren(tag=_ns('s','Branch')):
                self.appendChild(SQBLModuleNamedItem(branch,self))
        if self.element.tag == _ns('s','Branch'):
            logic = [i for i in self.element.iterchildren(tag=_ns('s','BranchLogic'))][0]
            for x in logic.iterchildren():
                self.appendChild(SQBLModuleNamedItem(x,self))
        if self.element.tag == _ns('s','ForLoop'):
            logic = [i for i in self.element.iterchildren(tag=_ns('s','LoopedLogic'))][0]
            for x in logic.iterchildren():
                self.appendChild(SQBLModuleNamedItem(x,self))
        if self.element.tag == _ns('s','QuestionGroup'):
            logic = [i for i in self.element.iterchildren(tag=_ns('s','GroupedQuestions'))][0]
            for x in logic.iterchildren():
                self.appendChild(SQBLModuleNamedItem(x,self))

    def data(self, column):  
        try:
            return self.element.get('name',self.itemData)
        except IndexError:  
            return None  

    def setData(self, data):
        self.element.set('name',data)
        self.itemData = data


def newModule(name):
    return """
        <QuestionModule xmlns="{s}"     
            name="{module_name}" version="1" >
            <ModuleLogic />  
        </QuestionModule>
            """.format(s=_namespaces['s'],
        module_name = name)


def newQuestion(name,lang):
    return """
      <Question xmlns="{s}" name="{question_name}_$numItems">
            <ResponseType>
                <Text />
            </ResponseType>
        </Question>
    """.format(s=_namespaces['s'],
        question_name = name)

def newStatement(name):
    return """
        <Statement xmlns="%s" name="%s_$numItems"/>
    """%(_namespaces['s'],name)

def newForLoop(name):
    return """
        <ForLoop xmlns="%s" name="%s_$numItems" question="">
            <LoopedLogic></LoopedLogic>
        </ForLoop>
    """%(_namespaces['s'],name)

def newBranch(name):
    return """
        <Branch xmlns="{s}" name="{branch_name}">
            <BranchLogic>
            </BranchLogic>
        </Branch>
    """.format( s=_namespaces['s'],
                branch_name = name,
                )

def newQuestionGroup(name,question="QuestionID"):
    # We allow this to be non-conformant by not including a condition, and assume the user will 'do the right thing'
    return """
      <QuestionGroup xmlns="{s}" name="{name}_$numItems">
            <GroupedQuestions>
            </GroupedQuestions>
        </QuestionGroup >
    """.format( s=_namespaces['s'],
                name=name,
                )
def newConditionalTree(name,question="QuestionID"):
    # We allow this to be non-conformant by not including a condition, and assume the user will 'do the right thing'
    return """
      <ConditionalTree xmlns="{s}" name="{name}_$numItems">
            <SequenceGuide>
            </SequenceGuide>
        </ConditionalTree>
    """.format( s=_namespaces['s'],
                name=name,
                )


class NewModuleItem(QtGui.QStandardItem):
    def __init__(self,name, helpPath,data):
        QtGui.QStandardItem.__init__(self,name)
        self.setData(data,QtCore.Qt.UserRole)
        self.helpPath = helpPath
    
    def getHelp(self):
        return self.helpPath

class NewItemsListModel(QtGui.QStandardItemModel):
    def __init__(self):
        QtGui.QStandardItemModel.__init__(self)
        
        self.icons = {
                _ns('s',"Statement"): QtGui.QIcon("icons/Statement.png"),
                _ns('s',"ConditionalTree"): QtGui.QIcon("icons/ConditionalTree.png"),
                _ns('s',"Question"):  QtGui.QIcon("icons/Question.png"),
                _ns('s',"ForLoop"):  QtGui.QIcon("icons/Loop.png"),
                _ns('s',"ModuleExitPoint"):  QtGui.QIcon("icons/StopModule.png"),
                _ns('s',"QuestionGroup"):  QtGui.QIcon("icons/QuestionGroup.png"),
                }

        parentItem = self.invisibleRootItem()
        self.numberOfNewItems = 100
        # List of New items:
        #   human name, namespace name,
        #   xpath to the help in the schema,
        #   new python object 
        newItems = [
                ("Question",_ns("s","Question"),
                    "//xs:complexType[@name='QuestionType']",
                    newQuestion("NewQuestion","en")),
                ("Statement",_ns("s","Statement",),
                    "//xs:element[@name='Statement']",
                    newStatement("NewStatement")),
                ("For Loop",_ns("s","ForLoop",),
                    "//xs:element[@name='ForLoop']",
                    newForLoop("NewForLoop")),
                ("Conditional Tree",_ns("s","ConditionalTree"),
                    "//xs:element[@name='ConditionalTree']",
                    newConditionalTree("NewTree")),
                ("Question Group",_ns("s","QuestionGroup"),
                    "//xs:element[@name='QuestionGroup']",
                    newQuestionGroup("NewGroup")),
            ]
        for name,tagname,helpPath,item in newItems:
            item = NewModuleItem(name,helpPath,item)
            item.setIcon(self.icons.get(tagname,None))
            item.setDragEnabled(True)
            parentItem.appendRow(item)
           
    def mimeData(self, indexes):
        self.numberOfNewItems = self.numberOfNewItems + 1
        # Only one thing can be selected, so we can just grab the first one, and serialise its XML
        index = indexes[0]
        data = str(self.data(index,QtCore.Qt.UserRole).toPyObject().toAscii())
        data = data.replace("$numItems",str(self.numberOfNewItems))
        mimedata = QtCore.QMimeData()
        mimedata.setData('text/xml+x-sqbl', data)
        # This is a new object and we need to make that clear when we drop it
        mimedata.setData('text/xml+x-sqbl+new', data)
        return mimedata

