from PyQt5 import QtWidgets, uic, QtGui
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainUI.ui', self)

        self.getWheels =  self.findChild(QtWidgets.QPushButton, 'addWheels')
        self.getWheels.clicked.connect(self.getWheelsClickListener)

        self.getDoors =  self.findChild(QtWidgets.QPushButton, 'addDoors')
        self.getDoors.clicked.connect(self.getDoorsClickListener)

        self.getMotor =  self.findChild(QtWidgets.QPushButton, 'addMotor')
        self.getMotor.clicked.connect(self.getMotorClickListener)

        self.getSize =  self.findChild(QtWidgets.QPushButton, 'addSize')
        self.getSize.clicked.connect(self.getSizeClickListener)

        self.wheels =  self.findChild(QtWidgets.QSpinBox, 'wheels')
        self.doors =  self.findChild(QtWidgets.QSpinBox, 'doors')

        self.motor =  self.findChild(QtWidgets.QComboBox, 'motor')
        self.size =  self.findChild(QtWidgets.QComboBox, 'size')

        self.FactList = self.findChild(QtWidgets.QListView, 'listView')
        self.listModel = QtGui.QStandardItemModel()
        self.FactList.setModel(self.listModel)
        self.show()

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


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
