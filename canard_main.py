from PyQt4 import QtCore, QtGui, QtWebKit
import pydot
import os, sys, StringIO
from SQBLWidgets import sqblUI, SQBLmodel, CanardPreferenceDialog
import SQBLWidgets
import ConfigParser
from lxml import etree
import Canard_settings as settings
AppSettings = QtCore.QSettings("sqbl.org", "Canard-App")

from SQBLWidgets.SQBLmodel import _ns

VERSION = "0.2.0B"
CRITICAL_SIZE = 50 # Number of nodes before refreshes get slow.

_APPWINDOWTITLE = "Canard Question Module Editor"

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    _INSTALLDIRECTORY = os.path.dirname(sys.executable) +"/"
#elif __file__:
#    _INSTALLDIRECTORY = os.path.dirname(__file__) +"/"
else:
    # Must be in development still
    _INSTALLDIRECTORY = "c:\\Users\\theodore\\Documents\\GitHub\\canard\\"

_INSTALLDIRECTORY = _INSTALLDIRECTORY.replace("\\","/")
_baseURL = _INSTALLDIRECTORY+"roxy"


class SQBLModulePane (QtGui.QWidget, sqblUI.module_pane.Ui_Form):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

class MainWindow(QtGui.QMainWindow, sqblUI.sqbl_main.Ui_MainWindow):
    def __init__(self,filename = None):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.centralArea.setWidth = 600

        self.saved      = True  # Flag to determine if we have unsaved changes
        self.model      = None  # The model for the TreeView
        self.newItems   = SQBLmodel.NewItemsListModel()  # The list of new things we can drag into the tree.
        self.newItemsList.setModel(self.newItems)
        self.newItemsList.setDragEnabled(True)

        self.threads = []
        self.filename = None
#        if filename is not None:
#            self.filename = filename #"../../sqbl-schema/Tests/dogDemographics.xml"
#            with open(self.filename) as f:
#                self.open(f.read())

        self.treeView.clicked.connect(self.setMainView)
        self.newItemsList.clicked.connect(self.setMainView)
        self.treeView.header().setResizeMode(0,QtGui.QHeaderView.ResizeToContents)
#        self.treeView.header().setStretchLastSection(False) # Not sure why I added this, so I'll leave it here for a little while. Its a UI thing anyway.
        self.treeView.setAcceptDrops(True)        
        self.treeView.header().setStretchLastSection(True)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.doTreeViewContextMenu)
        
        self.safeToRefresh = True

        # Subclassing is BULLSHIT
        def keyPressEvent(event,self=self.treeView):
            if event.key() == QtCore.Qt.Key_Delete:
                parent = self.model().getSelected().parent()
                parent.removeChild(self.model().getSelected())
                self.model().emit(QtCore.SIGNAL('layoutChanged()'))
            QtGui.QTreeView.keyPressEvent(self, event) 
        self.treeView.keyPressEvent = keyPressEvent
        
        self.actionNewModule.triggered.connect(self.newModule)
        self.actionOpen.triggered.connect(self.openFileDialog)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSaveAs.triggered.connect(self.saveFileAs)
        self.PreviewRefresh.clicked.connect(self.refreshPreview)
        self.copyImage.clicked.connect(self.copyFlowChartImage)
        #self.actionXXX.triggered.connect(self.YYY)

        self.actionRefeshPreviewers.triggered.connect(self.updateFlowchart)
        self.actionRefeshPreviewers.triggered.connect(self.refreshPreview)
        self.actionRefeshPreviewers.triggered.connect(self.refreshPreview)
        self.actionShowPreferences.triggered.connect(self.showPreferences)

        self.autoFlowchartRefresh = True
        self.actionAutoRefreshFlowchart.toggled.connect(self.setAutoFlowchartRefresh)
        self.actionAutoRefreshFlowchart.setChecked(self.autoFlowchartRefresh)

        #Connect more actions
        self.actionCreateNewWordsub.triggered.connect(self.addWordSub)

        # Connect import/export refreshers
        self.actionRefreshImport.triggered.connect(self.refreshImportMenu)
        self.refreshImportMenu()
        self.actionRefreshExport.triggered.connect(self.refreshExportMenu)
        self.refreshExportMenu()
         
        self.actionBlame.triggered.connect(self.vanityBox)
        self.actionAddLanguageGlobally.triggered.connect(self.addGlobalLanguage)
        self.actionFileABug.triggered.connect(self.fileBug)

        self.selected = None
        self.mainWidget = None
        self.setWindowIcon(QtGui.QIcon("icons/Canard.png"))

        # Get rid of stuff that we've built in the UI, but haven't finished coding
        self.unsupportedFeature(self.dataElementDock)
        self.unsupportedFeature(self.actionRefreshImport)
        self.unsupportedFeature(self.actionRefreshExport)
        self.unsupportedFeature(self.actionAutoRefreshPreviewer)
        self.unsupportedFeature(self.toolBarRichText)

        self.restoreGeometry(
                AppSettings.value("MainWindow/Geometry").toByteArray())
        #. app's State include Geometries of named toolbars and dockables:
        self.restoreState(AppSettings.value("MainWindow/State").toByteArray())


        # Everything is set up, lets make a new file...
        if filename is not None:
            self.openFile(filename)
        else:
            self.newModule()

    def addGlobalLanguage(self):
        newLang,success = SQBLWidgets.languagePicker.languagePickerDialog()
        if success and newLang is not "":
            self.model.addGlobalLanguage(newLang)

    def showPreferences(self):
        CanardPreferenceDialog.Dialog().exec_()

    def fileBug(self):
        import webbrowser
        webbrowser.open('https://github.com/LegoStormtroopr/canard/issues')
        

    def doTreeViewContextMenu(self, point):
        treeidx=self.treeView.indexAt(point)
        menu = QtGui.QMenu(self)
        tag = self.model.data(treeidx,"element").tag
        tag = tag.replace("{%s}"%SQBLmodel._namespaces['s'],"")
        print tag
        if tag == "WordSubstitutions":
            menu.addAction(self.actionCreateNewWordsub)
        x = menu.exec_(self.treeView.mapToGlobal(point))
        print x

    def addWordSub(self):
        self.model.addWordSub()

    def vanityBox(self):
        vanityText = """<html>
<head>
<meta name="qrichtext" content="1" />
</head>
<body>
<p>
<h3>Canard - Question Module Editor v{version}</h3>
</p>
<p>
<br>Released under GPLv3 Licence<br>
Details available at: <a href="http://github.com/LegoStormtroopr/canard">GitHub<a>
</p>
<p>
Read more about <a href="http://sqbl.org">SQBL</a> for more information on how Canard stores and manages questionnaire specifications.
</p>
<p>
Primary Developer: <a href="http:/about.me/legostormtroopr">Samuel Spencer</a>
</p>
</body>
</html>
""".format(version=VERSION)
        QtGui.QMessageBox.about(self,"About Virgil UI", vanityText )

    def refreshImportMenu(self):
        self.refreshPluginMenu("import", self.menuImport)

    def refreshExportMenu(self):
        self.refreshPluginMenu("export", self.menuExport)


    def refreshPluginMenu(self,pluginType,menu):
        for name in os.walk('./plugins/%s/'%(pluginType)).next()[1]:
            try:
                config = ConfigParser.RawConfigParser()
                config.read('./plugins/%s/%s/plugin.ini'%(pluginType,name))
                title = config.get('SQBL Plugin',"Name")
                runType = config.get('SQBL Plugin',"Type").lower()
                if runType not in ["import","export"]:
                    return #not an importer or exporter, so bail.
                action = QtGui.QAction("%s (%s)"%(title,name), self.menuImport)
                action.setData('./plugins/%s/%s'%(pluginType,name))
                action.triggered.connect(self.runImportExport)
                menu.addAction(action)
            except:
                #if the plugin folder has no ini file, just ignore it
                pass

    def runImportExport(self):
        #Thanks to below line for line 584 and on...
        # http://americiumdream.wordpress.com/cyb-dev/commented-pyqt-code-for-main-windows/
        action = self.sender()
        importDir = ""
        if isinstance(action, QtGui.QAction): #(paranoid sanity check)
            # the menu item's data is the filename we need:
            importDir = unicode(action.data().toString())
        else:
            return
        config = ConfigParser.RawConfigParser()
        config.read('./%s/plugin.ini'%importDir)
        name = config.get('SQBL Plugin',"Name")
        filetypes = config.get('SQBL Plugin',"Extensions")
        bf = config.get('SQBL Plugin',"Base File")
        extension = bf.rsplit('.',1)[-1].lower()
        runType = config.get('SQBL Plugin',"Type").lower()
        if runType not in ["import","export"]:
            return #not an importer or exporter, so bail. TODO: Maybe an error?
        if extension in ['xsl','xslt']:
            if runType == "import":
                filename = QtGui.QFileDialog.getOpenFileName(
                    self, 'Import - %s'%name, '.', filetypes
                    )
            elif runType == "export":
                filename = QtGui.QFileDialog.getSaveFileName(
                    self, 'Export - %s'%name, '.', filetypes
                    )
            if not filename:
                return #User hit cancel, so bail
            if runType == "import":
                with open(filename,"r") as f:
                    xml = etree.parse(f)
            elif runType == "export":
                xml = etree.fromstring(self.model.getXMLstring())
            with open("./%s/%s"%(importDir,bf)) as f:
                parser = etree.XMLParser(recover=True)
                xslt = etree.parse(f,parser)
                transform = etree.XSLT(xslt)
                out = unicode(transform(xml))
            if runType == "import":
                self.open(out)
            elif runType == "export":
                with open(filename,"w") as f:
                    f.write(out)

    def unsupportedFeature(self,item):
        item.setVisible(False) # Hides instantly
        item.deleteLater()     # Deletes after a small delay

    def setAutoFlowchartRefresh(self,state):
        state = True if state is True else False
        print state
        self.autoFlowchartRefresh = state

    def setSafeAutoFlowchartRefresh(self,state):
        msg = ""
        if state is not True:
            state = False # Just to be sure
            msg = "\n(Disabled due to document size)   "
        self.safeToRefresh = state
        self.actionAutoRefreshFlowchart.setEnabled(state)
        self.actionAutoRefreshFlowchart.setToolTip(
            str(self.actionAutoRefreshFlowchart.text()+msg)
          )


    def copyFlowChartImage(self):
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setPixmap(self.flowchart.pixmap())

    def updateLayout(self,newWidget):
        self.clearLayout()
        self.mainPanel = newWidget
        
        self.centralArea.addWidget(self.mainPanel)

        self.centralArea.update()
#        self.model.emit(QtCore.SIGNAL('layoutChanged()'))
#        self.model.emit(QtCore.SIGNAL('updateFlowchart()'))

    def clearLayout(self):
        if self.centralArea is not None:
            for i in reversed(range(self.centralArea.count())):
                self.centralArea.itemAt(i).widget().setParent(None)
            import sip

    def showItemHelp(self,selected):
        a = selected.internalPointer().parent()
        item = self.newItems.data(selected)
        # fuck it, i give in, need to know how to call these things, 

    def setMainView(self,selected):
        
        # Here selected is the current selected index.

        # Now get the new object
        self.model.setSelected(selected.internalPointer())
        self.selected = self.model.data(selected,role="element")

        newWidget = None
        if self.selected.tag == _ns("s","QuestionModule"):
            newWidget = SQBLWidgets.QuestionModule(self.selected,self.model)
        if self.selected.tag == _ns("s","Statement"):
            newWidget = SQBLWidgets.Statement(self.selected,self.model)
        if self.selected.tag == _ns("s","ConditionalTree"):
            newWidget = SQBLWidgets.ConditionalTree(self.selected,self.model)
        if self.selected.tag == _ns("s","Question"):
            newWidget = SQBLWidgets.Question(self.selected,self.model)
        if self.selected.tag == _ns("s","Branch"):
            newWidget = SQBLWidgets.Branch(self.selected,self.model)
        if self.selected.tag == _ns("s","ForLoop"):
            newWidget = SQBLWidgets.LoopFor(self.selected,self.model)
        if self.selected.tag == _ns("s","ModuleExitPoint"):
            newWidget = SQBLWidgets.StopModule(self.selected,self.model)
        if self.selected.tag == _ns("s","WordSub"):
            newWidget = SQBLWidgets.WordSub(self.selected,self.model)
        if self.selected.tag == _ns("s","QuestionGroup"):
            newWidget = SQBLWidgets.QuestionGroup(self.selected,self.model)
        if self.selected.tag == _ns("s","ModuleLogic"):
            newWidget = SQBLWidgets.ModuleLogic(self.selected,self.model)
        if newWidget is None:
            newWidget = SQBLWidgets.UnsupportedWidget()
        if newWidget is not None:
            self.updateLayout(newWidget)


    def newModule(self):
        self.filename = None
        self.open(SQBLmodel.newModule("NEW_MODULE"))
        self.updateTitle()

    def saveFileAs(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File As', '.')
        return self.saveFile()

    def saveFile(self):
        if self.filename is not None:
            with open(self.filename,"w") as f:
                f.write(self.model.getXMLstring())
                self.setSavedStatus(True)
        else:
            self.saveFileAs()
        self.updateTitle()

    def openFile(self,filename):
        try:
            with open(filename,"r") as f:
                self.filename = filename
                self.open(f.read())
        except IOError as e:
            self.filename = None
            QtGui.QMessageBox.critical(self,
                    "Unable to open the requested file",
                    "The file %s was unable to be opened, the error message is included below.\n\n%s"%(filename,str(e))
                    )
            self.newModule()

        self.saved = True


    def openFileDialog(self):
        #trigger save question here
        canOpenFile = self.savedDialog(message="Do you want to save the changes before opening another document?")
        if canOpenFile:
            filename = QtGui.QFileDialog.getOpenFileName(
                    self, 'Open Question Module', '.',
                    "Question Modules (*.sqbl *.qbl);;All XML Files (*.xml) ;;All Files (*.*)"
                    )
            if filename:
                self.openFile(filename)

    # Since we might be opening local or remote files, which will use different interfaces, we have an abstract method which takes and prepares an XML string from "someplace".
    def open(self,xml):
        from lxml import etree
        try:
            sqbl_xsd = etree.XMLSchema(etree.parse("./sqbl/sqbl.xsd"))

            self.model = SQBLmodel.QuestionModule(xml)
            #Catch updates to the model and update views.

            self.treeView.setModel(self.model)
            self.connect(self.model, QtCore.SIGNAL('dataChanged()'), self.updateTitle)
            self.connect(self.model, QtCore.SIGNAL('dataChanged()'), self.thingsChanged)
            self.connect(self.model, QtCore.SIGNAL('layoutChanged()'), self.thingsChanged)
            self.connect(self.model, QtCore.SIGNAL('layoutChanged()'), self.requestFlowchartUpdate)
            self.model.emit(QtCore.SIGNAL('layoutChanged()'))
            self.treeView.expandToDepth(1)
            self.treeView.resizeColumnToContents(0)
            self.treeView.header().setResizeMode(0,QtGui.QHeaderView.Stretch | QtGui.QHeaderView.ResizeToContents)

            if self.model.totalChildren() > CRITICAL_SIZE :
                QtGui.QMessageBox.critical(self,
                "The size of this Question Module is too big.",
                "This model is too large for automatic refreshes of the previewer.\nYou can still manually update the flowchart and webpage preview, but it may take some time."
                        )
                self.setSafeAutoFlowchartRefresh(False)

        except etree.DocumentInvalid as e:
            QtGui.QMessageBox.critical(self,
                "Requested SQBL Document is not valid",
                "The file '%s' could be opened, but does not contain a valid SQBL Question Module.\n You can try opening the file again, and if this error returns, the file may be corrupted or not a SQBL document.\n\nThe error message is included below.\n\n%s"%(self.filename,str(e))
                    )
            self.newModule()
        self.setSavedStatus(True)

    def setSavedStatus(self,status):
        #We override these again, to make the title bar look nice.
        self.saved = bool(status) #Cast to a bool.
        self.updateTitle()

    def updateTitle(self):
        name = self.model.getModuleName()
        ast = ""
        if not self.saved:
            # If it's unsaved lets put in a nice reminder in the title bar
            ast = "*"

        filename = self.filename
        if filename is None:
            # If its a new file, lets make that very clear
            filename = "Unsaved"

        self.setWindowTitle("%s - %s (%s)%s"%(_APPWINDOWTITLE,name,filename,ast))

    def thingsChanged(self):
        self.setSavedStatus(False)
        #self.updateFlowchart()
        #self.refreshPreview()

    # We reply True if the file is saved, or the user doesn't want to keep the changes
    # False if the use cancels or cancels during the save process.
    def savedDialog(self,message=""):
        reply = True
        if not self.saved:
            reply = QtGui.QMessageBox.question(self, 'Unsaved Changes', "This file has unsaved changes.\n%s\n\nIf you don't save your changes they be lost." % message, QtGui.QMessageBox.Discard, QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Save)
            if reply == QtGui.QMessageBox.Cancel:
                # user hits cancel, don't open a new file
                reply = False 
            if reply == QtGui.QMessageBox.Save:
                # user hits save, save file and open a new file
                reply = self.saveFile()
            if reply == QtGui.QMessageBox.Discard:
                # user hits discard, just open a new file
                reply = True
        return reply

    def closeEvent(self, event):
        safeToClose = self.savedDialog(message="Do you want to save the changes to this document before closing?")
        if safeToClose:
            event.accept()
            AppSettings.setValue("MainWindow/Geometry", QtCore.QVariant(
                              self.saveGeometry()))
            AppSettings.setValue("MainWindow/State", QtCore.QVariant(
                              self.saveState()))            
        else:
            event.ignore()            

    def requestFlowchartUpdate(self):
        x = self.model.totalChildren()
        # if the model is too big don't allow automatic updates
        if x > CRITICAL_SIZE: return
        print self.autoFlowchartRefresh
        if not self.autoFlowchartRefresh: return
        self.updateFlowchart()
        
    def updateFlowchart(self):
        from lxml import etree
        import tempfile
        with open("roxy/SQBL_to_Skips.xsl") as f:
            xslt = etree.XML(f.read())
            transform = etree.XSLT(xslt)
            data = self.model.getXMLetree()
            out = etree.XML(str(transform(data)))
            skips = out.xpath('//skip:skips2', namespaces={"skip":"http://legostormtoopr/skips"})[0]

        flow = pydot.Dot(graph_type='digraph',fontsize=7)

        for link in skips.iterchildren(tag="{http://legostormtoopr/skips}link"):
            shape = "oval"
            edgeColor = "black"
            if link.get('type') == "StopModule":
                shape="doubleoctagon"
                edgeColor = "crimson"
            flow.add_node(pydot.Node(link.get('from'), \
                shape=shape, \
                label=link.get('from'), \
                fontsize=8, \
                fontname="Helvetica", \
              ))
            from_ = link.get('from', default="Start")
            to_   = link.get('to')
            if to_ == "":
                to_ = "__End__"

            label = link.get('condition',None)
            # This comparison will only work if the condition is not 'otherwise', so we don't need a case to make the label otherwise ;)
            if label is None:
                conditions = []
                for c in link.iterchildren(tag="{http://legostormtoopr/skips}condition"):
                    comp = SQBLWidgets.comparisonMap(c.get('comparator'))

                    value = c.text
                    conditions.append("%s %s"%(comp, value))
                label = " "+", ".join(conditions)

            flow.add_edge(pydot.Edge(from_,to_,label=label,fontsize=7,color=edgeColor))


        for sg in skips.iterchildren(tag="{http://legostormtoopr/skips}sequenceGuide"):
            flow.add_node(pydot.Node(sg.get('from'), \
                shape="diamond", \
                label=sg.get('from'), \
                fontsize=10, \
                fontname="Helvetica", \
              ))
            from_ = sg.get('from', default="Start")
            for link in sg.iterchildren(tag="{http://legostormtoopr/skips}link"):
                to_   = link.get('to', default="__End__")
                if to_ == "":
                    to_ = "__End__"
                flow.add_edge(pydot.Edge(from_,to_))

                done = [] # Conditions which we've accounted for
            for cond in sg.xpath('.//skip:condition', namespaces={"skip":"http://legostormtoopr/skips"}):

                q = cond.get('question',default=None)
                if q is not None and q not in done:
                    flow.add_edge(pydot.Edge(q,from_,color="gray",style="dashed"))
                    done.append(q)

        for sg in skips.iterchildren(tag="{http://legostormtoopr/skips}loop"):
            flow.add_node(pydot.Node(sg.get('from'), \
                shape="rectangle", \
                label=sg.get('from'), \
                fontsize=10, \
                fontname="Helvetica", \
              ))
            from_ = sg.get('from')
            to_ = sg.get('to')
            inner_ = sg.get('innerchild')
            question_ = sg.get('question')

            flow.add_node(pydot.Node("%s__LOOP_END"%from_, \
                shape="rectangle", \
                label='%s\nLoop End'%from_, \
                fontsize=8, \
                fontname="Helvetica", \
              ))
            flow.add_edge(pydot.Edge(question_,from_,color="gray",style="dashed"))
            flow.add_edge(pydot.Edge(from_,inner_))
            flow.add_edge(pydot.Edge("%s__LOOP_END"%from_,from_,style="dashed"))
            flow.add_edge(pydot.Edge("%s__LOOP_END"%from_,to_))


        img = tempfile.NamedTemporaryFile().name
        flow.write_png(img)
        myPixmap = QtGui.QPixmap(img) #.scaledToWidth(self.flowchart.width())
        self.flowchart.setPixmap(myPixmap)

    def refreshPreview(self):
        from lxml import etree
        #with open("../roxy-sqbl-instrument-creator/SQBL-Module_to_HTML.xsl") as f:
        with open("roxy/SQBL-Module_to_XForm.xsl") as f:

            class FileResolver(etree.Resolver):
                def resolve(self, url, pubid, context):
                    return self.resolve_filename(url, context)

            parser = etree.XMLParser()
            parser.resolvers.add(FileResolver())

            xslt = etree.parse(f,parser)
            transform = etree.XSLT(xslt)
            data = self.model.getXMLetree()


            #out = str(transform(data,rootdir=etree.XSLT.strparam(_baseURL.replace("/","\\"))))
            out = str(transform(data,rootdir=etree.XSLT.strparam(_INSTALLDIRECTORY+"./roxy/")))
            out = etree.XML(out)
          # Disabling XForms for the time being
            with open("roxy/xsltforms-beta2/xsltforms/xsltforms.xsl") as x:
                xsltforms = etree.XML(x.read())
                xsltforms = etree.XSLT(xsltforms)
                out = xsltforms(out)

            self.Previewer.setContent(str(out), "text/html", QtCore.QUrl(_baseURL))

    # Defunct threading attempt
    # Will try again later, for now, forcing a user to hit refresh aint all bad.
    def refreshPreviewThread(self):
        pass
        
    def updatePreview(self,html):
        self.Previewer.setHtml(str(html))
        

class XSLTRunner(QtCore.QThread):
    def __init__(self,xml,transformer,parent):
        QtCore.QThread.__init__(self)
        self.xml = xml
        self.transformer = transformer
        self.parent = parent

    def transform(self):
        from lxml import etree
        return etree.XML(str(self.transformer(self.xml)))

    def kill(self):
        self.terminate()

    def run(self):
            from lxml import etree
            out = self.transform()
            #with open("../roxy/xsltforms-beta2/xsltforms/xsltforms.xsl") as x:
            #    xsltforms = etree.XML(x.read())
            #    xsltforms = etree.XSLT(xsltforms)
            #    out = xsltforms(out)
            self.parent.emit(QtCore.SIGNAL('updatePreviewer(QString)'), QString(out) )

def main(filename=None):
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=MainWindow(filename=filename)
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


