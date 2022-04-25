from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainUI.ui', self)

        ######################################### vehicles items declaration #######################################################
        #wheels button
        self.getWheels =  self.findChild(QtWidgets.QPushButton, 'addWheels')
        self.getWheels.clicked.connect(self.getWheelsClickListener)

        #doors button
        self.getDoors =  self.findChild(QtWidgets.QPushButton, 'addDoors')
        self.getDoors.clicked.connect(self.getDoorsClickListener)

        #motor button
        self.getMotor =  self.findChild(QtWidgets.QPushButton, 'addMotor')
        self.getMotor.clicked.connect(self.getMotorClickListener)

        #size button
        self.getSize =  self.findChild(QtWidgets.QPushButton, 'addSize')
        self.getSize.clicked.connect(self.getSizeClickListener)

        #spinners declaration
        self.wheels =  self.findChild(QtWidgets.QSpinBox, 'wheels')
        self.doors =  self.findChild(QtWidgets.QSpinBox, 'doors')

        #combo boxes declatation
        self.motor =  self.findChild(QtWidgets.QComboBox, 'motor')
        self.size =  self.findChild(QtWidgets.QComboBox, 'size')

        #list view declaration with its model
        self.FactListVehicles = self.findChild(QtWidgets.QListView, 'listView')
        self.FactListVehicles.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listModel = QtGui.QStandardItemModel()
        self.FactListVehicles.setModel(self.listModel)

        #remove from fact list button 
        self.removeVehicleFact =  self.findChild(QtWidgets.QPushButton, 'removeVehicleFact')
        self.removeVehicleFact.clicked.connect(self.removeVehicleFactClickListener)
        #reset fact list button 
        self.resetFacts =  self.findChild(QtWidgets.QPushButton, 'resetFacts')
        self.resetFacts.clicked.connect(self.resetFactsClickListener)

        ####################################### medical diagnosis items declaration #######################################################
        #fever spinner declaration
        self.fever =  self.findChild(QtWidgets.QDoubleSpinBox, 'fever')

        #combo boxes declatation
        self.pain =  self.findChild(QtWidgets.QComboBox, 'pain')
        self.visible =  self.findChild(QtWidgets.QComboBox, 'visible')
        self.common =  self.findChild(QtWidgets.QComboBox, 'common')

        #button declaration
        #pain button
        self.getPain =  self.findChild(QtWidgets.QPushButton, 'addPain')
        self.getPain.clicked.connect(self.getPainClickListener)

        #visible symptoms button
        self.getVisible =  self.findChild(QtWidgets.QPushButton, 'addVisible')
        self.getVisible.clicked.connect(self.getVisibleClickListener)

        #common symptoms button
        self.getCommon =  self.findChild(QtWidgets.QPushButton, 'addCommon')
        self.getCommon.clicked.connect(self.getCommonClickListener)

        #fever button
        self.getFever =  self.findChild(QtWidgets.QPushButton, 'addFever')
        self.getFever.clicked.connect(self.getFeverClickListener)

        #fact list declaration
        #list view declaration with its model
        self.FactListSymptoms = self.findChild(QtWidgets.QListView, 'symptomsList')
        self.FactListSymptoms.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.sympModel = QtGui.QStandardItemModel()
        self.FactListSymptoms.setModel(self.sympModel)

        #remove from fact list button 
        self.removeSymptom =  self.findChild(QtWidgets.QPushButton, 'removeSymptom')
        self.removeSymptom.clicked.connect(self.removeSymptomClickListener)
        #reset fact list button 
        self.resetSymptoms =  self.findChild(QtWidgets.QPushButton, 'resetSymptoms')
        self.resetSymptoms.clicked.connect(self.resetSymptomsClickListener)
        
        self.show()
    
    #button click listeners
    ################################################## vehicles ###################################################
    def getWheelsClickListener(self):
        item = QtGui.QStandardItem(f'wheels = {self.wheels.value()}')
        self.listModel.appendRow(item)
    def getDoorsClickListener(self):
        item = QtGui.QStandardItem(f'doors = {self.doors.value()}')
        self.listModel.appendRow(item)
    def getMotorClickListener(self):
        item = QtGui.QStandardItem(f'motor = {self.motor.currentText()}')
        self.listModel.appendRow(item)
    def getSizeClickListener(self):
        item = QtGui.QStandardItem(f'size = {self.size.currentText()}')
        self.listModel.appendRow(item)
    def removeVehicleFactClickListener(self):
        if len(self.FactListVehicles.selectedIndexes()) > 1:
            for items in reversed(sorted(self.FactListVehicles.selectedIndexes())):
                self.listModel.takeRow(items.row()) 
    def resetFactsClickListener(self):
        self.listModel.removeRows( 0, self.listModel.rowCount() )
        
    
    ###################################### Medical diagnosis ##############################################
    def getPainClickListener(self):
        item = QtGui.QStandardItem(f'{self.pain.currentText()}')
        self.sympModel.appendRow(item)
    def getVisibleClickListener(self):
        item = QtGui.QStandardItem(f'{self.visible.currentText()}')
        self.sympModel.appendRow(item)
    def getCommonClickListener(self):
        item = QtGui.QStandardItem(f'{self.common.currentText()}')
        self.sympModel.appendRow(item)
    def getFeverClickListener(self):
        item = QtGui.QStandardItem(f'Temperature = {self.fever.value()}')
        self.sympModel.appendRow(item)
    def removeSymptomClickListener(self):
        if len(self.FactListSymptoms.selectedIndexes()) > 1:
            for items in reversed(sorted(self.FactListSymptoms.selectedIndexes())):
                self.sympModel.takeRow(items.row()) 
    def resetSymptomsClickListener(self):
        self.sympModel.removeRows( 0, self.sympModel.rowCount() )

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
