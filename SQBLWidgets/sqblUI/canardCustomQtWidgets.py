from PyQt4 import QtCore, QtGui

# Thanks for the below to http://stackoverflow.com/questions/3901829/pyqt-qtablewidget-keyboard-events-while-editing
# Allows enter to cycle edits through columns and to the next row.
# On the last row it throws a signal that its at the end, this allows other classes to
#   capture this and use it, e.g. to add a new row at the end.
class ReturnSupportedTableWidget(QtGui.QTableWidget):
    cycleFromLastCell = QtCore.pyqtSignal()

    def __init__(self,parent):
        QtGui.QTableWidget.__init__(self, parent)

        self.keys = [QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab]

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyRelease and event.key() in self.keys:
            self._moveSelection(event.key())

        return QtGui.QTableWidget.event(self, event)

    def _moveSelection (self, key):
        row = self.currentRow()
        col = self.currentColumn()
        print row,col

        if key == QtCore.Qt.Key_Return :
            col += 1
            if col == self.columnCount():
                col = 0
                row += 1
            if row == self.rowCount():
                # We don't want to change the row and col here, let the catcher do it.
                self.cycleFromLastCell.emit()
                return
        else:
            return

        self.setCurrentCell(row, col)
        self.edit(self.currentIndex())

