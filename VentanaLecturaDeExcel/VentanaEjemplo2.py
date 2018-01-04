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


        self.tableView = QtWidgets.QTableView(self.centralWidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 3)


        #self.openTable = QtWidgets.QPushButton(self.centralWidget)
        #self.openTable.setObjectName("openTable")
        #self.gridLayout.addWidget(self.openTable, 1, 0, 1, 1)
        #self.openTable.clicked.connect(self.CargaTabla)

        label1 = QtWidgets.QLabel("Example content contained in a tab.")
        label2 = QtWidgets.QLabel("More example text in the second tab.")

        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(label1, "Tab 1")
        tabwidget.addTab(label2, "Tab 2")
        #layout.addWidget(tabwidget, 0, 0)
        self.gridLayout.addWidget(tabwidget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 534, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menuBar)

        self.extractAction = QtWidgets.QAction(QtGui.QIcon("./Iconos/open.png"),'Open file',MainWindow)
        self.extractAction.setShortcut("Ctrl+o")
        self.extractAction.triggered.connect(self.CargaTabla)

        self.extractAction2 = QtWidgets.QAction(QtGui.QIcon("./Iconos/save.png"),'Save file',MainWindow)
        self.extractAction2.setShortcut("Ctrl+s")
        self.extractAction2.triggered.connect(self.GuardarTabla)

        self.extractAction3 = QtWidgets.QAction(QtGui.QIcon("./Iconos/work.png"),'Optimization',MainWindow)
        self.extractAction3.setShortcut("Ctrl+w")
        self.extractAction3.triggered.connect(self.OptimizarTabla)

        self.extractAction4 = QtWidgets.QAction(QtGui.QIcon("./Iconos/clean.png"),'Clean all',MainWindow)
        self.extractAction4.setShortcut("Ctrl+c")
        self.extractAction4.triggered.connect(self.LimpiarTabla)



        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        self.mainToolBar.addAction(self.extractAction)
        self.mainToolBar.addAction(self.extractAction2)
        self.mainToolBar.addAction(self.extractAction3)
        self.mainToolBar.addAction(self.extractAction4)

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
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))

    def OptimizarTabla(self):
        print("La tabla se optimiza")

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
