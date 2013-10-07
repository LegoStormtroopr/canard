from PyQt4 import QtCore
import sqlite3

class TUSLCache:
    def __init__(self):
        self.conn = sqlite3.connect('TUSLCache.db')
        self.curr = self.conn.cursor()
        self.curr.execute('''CREATE TABLE IF NOT EXISTS cache
             (uri TEXT, type TEXT, obj TEXT, PRIMARY KEY (uri,type))''')
    def __del__(self):
        self.conn.close()

    def setProperty(self,uri,obj):
        return self.insertCache(uri,'Property',obj)
    def getProperty(self,uri=None):
        return self.retrieveCache(uri,'Property')

    def setObjectClass(self,uri,obj):
        return self.insertCache(uri,'ObjectClass',obj)
    def getObjectClass(self,uri=None):
        return self.retrieveCache(uri,'ObjectClass')

    def insertCache(self,uri,objType,obj):
        self.curr.execute('INSERT OR REPLACE INTO cache VALUES (?,?,?)',(uri,objType,obj))
        self.conn.commit()
    def retrieveCache(self,uri,objType):
        x = None
        if uri is None:
            x = []
            for c in self.curr.execute('SELECT obj FROM cache WHERE type=?',[objType]):
                x.append(c[0])
        else:
            self.curr.execute('SELECT obj FROM cache WHERE uri=? and type=?',(uri,objType))
            x = self.curr.fetchone() 
            if x is not None: # Will be none if no reference is found.
                x = x[0] # get the first object in the tuple, as its the only one
        return x

TUSLObjectCache = TUSLCache()
AppSettings = QtCore.QSettings("sqbl.org", "Canard-App")

def getPref(key,default=None):
    return AppSettings.value(key,default).toPyObject()

def setPref(key,value):
    return AppSettings.setValue(key,value)

if getPref('displayLanguage') is None:
    setPref('displayLanguage','en')

if getPref('defaultObjectLangauges') is None:
    setPref('defaultObjectLangauges',['en','de'])


