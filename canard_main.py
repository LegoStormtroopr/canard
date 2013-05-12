from PyQt4 import QtCore, QtGui, QtWebKit
import pydot
import os, sys, StringIO
from SQBLWidgets import sqblUI
from SQBLWidgets import SQBLmodel
import SQBLWidgets

import Canard_settings as settings

from SQBLWidgets.SQBLmodel import _ns

VERSION = "0.0.1B"

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
print _INSTALLDIRECTORY
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
        self.treeView.header().setResizeMode(0,QtGui.QHeaderView.ResizeToContents)
#        self.treeView.header().setStretchLastSection(False) # Not sure why I added this, so I'll leave it here for a little while. Its a UI thing anyway.
        self.treeView.setAcceptDrops(True)        
        self.treeView.header().setStretchLastSection(True)

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
         
        self.actionBlame.triggered.connect(self.vanityBox)

        self.selected = None
        self.mainWidget = None
        self.setWindowIcon(QtGui.QIcon("icons/Canard.png"))

        # Get rid of stuff that we've built in the UI, but haven't finished coding
        self.unsupportedFeature(self.webServerDock)
        self.unsupportedFeature(self.dataElementDock)
        self.unsupportedFeature(self.toolFormat)


        # Everything is set up, lets make a new file...
        if filename is not None:
            self.openFile(filename)
        else:
            self.newModule()

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
Details available at: <a href="http://code.google.com/p/virgil-ui/">GitHub<a>
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


    def unsupportedFeature(self,item):
        item.setVisible(False) # Hides instantly
        item.deleteLater()     # Deletes after a small delay


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
            sqbl_xsd.assertValid(etree.parse(StringIO.StringIO(xml)))

            self.model = SQBLmodel.QuestionModule(xml)
            #Catch updates to the model and update views.

            self.treeView.setModel(self.model)
            self.connect(self.model, QtCore.SIGNAL('dataChanged()'), self.updateTitle)
            self.connect(self.model, QtCore.SIGNAL('dataChanged()'), self.thingsChanged)
            self.connect(self.model, QtCore.SIGNAL('layoutChanged()'), self.thingsChanged)
            self.connect(self.model, QtCore.SIGNAL('layoutChanged()'), self.updateFlowchart)
            self.model.emit(QtCore.SIGNAL('layoutChanged()'))
            self.treeView.expandToDepth(1)
            self.treeView.resizeColumnToContents(0)
            self.treeView.header().setResizeMode(0,QtGui.QHeaderView.Stretch | QtGui.QHeaderView.ResizeToContents)

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
        else:
            event.ignore()            

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


