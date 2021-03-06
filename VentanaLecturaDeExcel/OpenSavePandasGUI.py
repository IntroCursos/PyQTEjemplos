
#pyuic5 -x mainwindow.ui -o output.py

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PandasData import Mi_tabla
import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(534, 379)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.openTable = QtWidgets.QPushButton(self.centralWidget)

        self.openTable.setObjectName("openTable")
        self.gridLayout.addWidget(self.openTable, 1, 0, 1, 1)
        self.openTable.clicked.connect(self.CargaTabla)

        self.tableView = QtWidgets.QTableView(self.centralWidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 3)

        self.clearTable = QtWidgets.QPushButton(self.centralWidget)
        self.clearTable.setObjectName("clearTable")
        self.gridLayout.addWidget(self.clearTable, 1, 1, 1, 1)
        self.clearTable.clicked.connect(self.LimpiarTabla)

        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 2)

        self.saveTable = QtWidgets.QPushButton(self.centralWidget)
        self.saveTable.setObjectName("saveTable")
        self.gridLayout.addWidget(self.saveTable, 1, 2, 1, 1)
        self.saveTable.clicked.connect(self.GuardarTabla)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 534, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClear)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.openTable.setText(_translate("MainWindow", "OpenTable"))
        self.clearTable.setText(_translate("MainWindow", "Clear Table"))
        self.saveTable.setText(_translate("MainWindow", "Save Table"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))

    def CargaTabla(self):
        #table = QtWidgets.QTableView()
        df =Mi_tabla()
        #df = pd.read_excel("./tabla.xlsx",sheetname="hoja1")
        mymodel = PandasModel(df)
        self.tableView.setModel(mymodel)

    def LimpiarTabla(self):

        self.tableView.setModel(None)

    def GuardarTabla(self):
        mymodel = self.tableView.model()
        print (type(mymodel) )
        print (type(mymodel._data) )
        print (len(mymodel._data.values))
        print (mymodel._data.values[0][0])
        df = mymodel._data
        #df.to_excel('foo.xlsx', sheet_name='Sheet1')
        print (df.index)
        # Specify a writer
        writer = pd.ExcelWriter('example2.xlsx', engine='xlsxwriter')
        # Write your DataFrame to a file
        #df.to_excel(writer, 'Sheet1')
        df.to_excel(writer, sheet_name='Sheet1')
        # Save the result
        writer.save()
        print("Segun eso se guardo")


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                if(index.column() != 0):
                    #return str('%.2f'%self._data.values[index.row()][index.column()])
                    return str(self._data.values[index.row()][index.column()])
                else:
                    return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[section]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return str(self._data.index[section])
        return None
    """
    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= QtCore.Qt.ItemIsSelectable
        flags |= QtCore.Qt.ItemIsEnabled
        return flags
    """

    def setData(self, index, value, role):
        self._data.iloc[[index.row()],[index.column()] ] = value
        return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
