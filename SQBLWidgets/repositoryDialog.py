import sqblUI
from PyQt4 import QtCore, QtGui
from SQBLmodel import _ns, _namespaces 
from lxml import etree
import isoLangCodes
import logging
from Canard_settings import TUSLObjectCache as cache

class repoDialog(QtGui.QDialog, sqblUI.repositorySearch.Ui_Dialog):
    def __init__(self,parent=None,objectType=None,repositories=[],language='en'):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.language = language
        self.items = None
        self.currentURI = None
        if objectType is not None:
            self.objectTypeValue = objectType
            self.objectType.setVisible(False)
            self.objectTypeLabel.setVisible(False)
        for repository in repositories:
            print repository
            self.repositoryURLs.addItem(repository)

        self.search.clicked.connect(self.doSearch)
        self.retrievedItems.itemSelectionChanged.connect(self.updateDesc)

    def doSearch(self):
        self.retrievedItems.clear()
        import urllib2
        url = self.createURL()
        repo = self.repositoryURLs.currentText()
        try:
            x = urllib2.urlopen(url)
            self.items = etree.fromstring(x.read())
            print x
        except Exception as e:
            QtGui.QMessageBox.warning(self, 
            'Repository unavailable - %s'% repo,
            "The selected repository (%s) is unreachable, you can click search to try again. But if this dialog returns there may be a network problem between this machine and the repository.\nDouble check the address is correct, and if you are able to access the internet fine, you may need to contact your systems administrator.\nThe full error has been logged in the install directory if more information is needed."% repo,
             QtGui.QMessageBox.Ok)
            logging.warning('Could not open %s -- %s ' % (repo,str(e)))
            pass
        #print x.read()
        else:
            for i in self.items:
                name = i.xpath("t:TextComponent[@xml:lang='%s']/t:Name"%self.language,namespaces=_namespaces)[0].text
                date = i.get('versionDate')
                self.retrievedItems.addItem("%s - (%s)"%(name,date))

    def createURL(self):
        repository = self.repositoryURLs.currentText()
        searchTerms = self.searchTerms.text()
        if self.objectType.isVisible():
            objectType = self.objectType.currentText()
        else:
            objectType = self.objectTypeValue
        return "%s/%s/?s=%s"%(repository,objectType,searchTerms)

    def updateDesc(self):
        self.selected = self.retrievedItems.currentRow()
        current = self.items[self.selected]
        self.currentURI = current.get('uri')
        name = current.xpath("t:TextComponent[@xml:lang='%s']/t:Name"%self.language,namespaces=_namespaces)[0].text
        desc = current.xpath("t:TextComponent[@xml:lang='%s']/t:Description"%self.language,namespaces=_namespaces)[0].text
        text = "<b><a href='{url}'>{name}</a></b><p>{desc}</p>".format(
                url = current.get('additionalInformation'),
                name = name,
                desc = desc
                )
        self.itemDetails.setText(text)

    def getValues(self):
        # Add Object to the cache
        repository = self.repositoryURLs.currentText()
        if self.objectType.isVisible():
            objectType = self.objectType.currentText()
        else:
            objectType = self.objectTypeValue
        cache.insertCache(uri=self.currentURI,objType=objectType,obj=etree.tostring(self.items[self.selected]))

        return (self.currentURI,self.items[self.selected])

# Dialog test frame
def main():
    import os, sys
    logging.basicConfig(
            filename='canard.log',
            filemode='w',
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    
    app = QtGui.QApplication(sys.argv)
    dlg = repoDialog(objectType="ObjectClass",
                repositories=['http://localhost:8080']
            )
    if dlg.exec_():
        values = dlg.getValues()
        print values
    sys.exit()
    

