from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys

###################################   test with the expert system
from itertools import cycle
from experta import *
import experta as experta


getFridges = []
fridge_features = []
getVehicle = []
getDiagnosis = []
invocated_rules = []

class Facts(Fact):
	pass

class myEngine(KnowledgeEngine):
################################################################################################################################
################################################# fridge rules ########################################################
	@Rule(Facts(f_doors = P(lambda nb: nb <= 3)))
	def FrenchFridge(self):
		engineV.declare(Facts(french_fridge = True))
	@Rule(Facts(hi_temp = P(lambda nb: nb <= (-18))))
	def Freezer(self):
		engineV.declare(Facts(type = 'Freezer'))
	@Rule(Facts(hi_temp = P(lambda nb: nb > (-18))))
	def Fridge(self):
		engineV.declare(Facts(type = 'Fridge'))
	@Rule(Facts(type = 'Fridge'), Facts(lo_temp = P(lambda nb: nb <= (-18))))
	def HasFreezer(self):
		engineV.declare(Facts(has_freezer = True))
	@Rule(Facts(type = 'Fridge'), Facts(lo_temp = P(lambda nb: nb > (-18))))
	def NoFreezer(self):
		engineV.declare(Facts(has_freezer = False))
	@Rule(Facts(size = 'Large'), Facts(type = 'Freezer'))
	def ChestFreezer(self):
		getFridges.append("Chest Freezer")
	@Rule(Facts(size = 'Small'), Facts(type = 'Freezer'))
	def UprightFreezer(self):
		getFridges.append("Upright Freezer")
	@Rule(Facts(size = 'Small'), Facts(f_doors = 1), Facts(has_freezer = False))
	def MiniFridge(self):
		getFridges.append("Mini Fridge")
	@Rule(Facts(size = 'Large'), Facts(f_doors = 2), Facts(has_freezer = True))
	def SideBySide(self):
		getFridges.append("Side-By-Side Fridge")
	@Rule(Facts(size = 'Large'), Facts(french_fridge = True), Facts(has_freezer = True))
	def FrenchDoorFridge(self):
		getFridges.append("French Doors Fridge")
	@Rule(Facts(size = 'Medium'), Facts(f_doors = 2), Facts(has_freezer = True))
	def StandardFridge(self):
		getFridges.append("Standard Fridge")
	@Rule(Facts(size = 'Medium'), Facts(f_doors = 1), Facts(has_freezer = False))
	def SimpleFridge(self):
		getFridges.append("Simple Fridge")
	@Rule(Facts(size = 'Large'),Facts(french_fridge = True), Facts(features__tablet =  1), Facts(has_freezer = True))
	def SmartFridge(self):
		getFridges.append("Smart Fridge")
	@Rule(Facts(size = 'Extra Large'), Facts(has_freezer = False), Facts(f_doors = 2))
	def ColumnFridge(self):
		getFridges.append("Column Fridge")
	@Rule(Facts(features__waterdispenser=1))
	def FeatureWater(self):
		fridge_features.append("Water dispenser")
	@Rule(Facts(features__icedispenser=1))
	def FeatureIce(self):
		fridge_features.append("Ice dispenser")
	@Rule(Facts(features__tablet=1))
	def FeatureTablet(self):
		fridge_features.append("Tablet")

engineV = myEngine()
		
#################################################################################################################################
############################################### G U I ###########################################################################

class Ui(QtWidgets.QMainWindow):
	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('multi_agents.ui', self)

		######################################### items declaration #######################################################
		################################## Buttons
		#size button
		self.add_size =  self.findChild(QtWidgets.QPushButton, 'add_size')
		self.add_size.clicked.connect(self.addSizeClickListener)

		#doors button
		self.add_doors =  self.findChild(QtWidgets.QPushButton, 'add_doors')
		self.add_doors.clicked.connect(self.addDoorsClickListener)

		#max temp button
		self.add_max_temp =  self.findChild(QtWidgets.QPushButton, 'add_max_temp')
		self.add_max_temp.clicked.connect(self.addMaxTempClickListener)

		#min temp button
		self.add_min_temp =  self.findChild(QtWidgets.QPushButton, 'add_min_temp')
		self.add_min_temp.clicked.connect(self.addMinTempClickListener)

		#min price button
		self.add_min_price =  self.findChild(QtWidgets.QPushButton, 'add_min_price')
		self.add_min_price.clicked.connect(self.addMinPriceClickListener)

		#max price button
		self.add_max_price =  self.findChild(QtWidgets.QPushButton, 'add_max_price')
		self.add_max_price.clicked.connect(self.addMaxPriceClickListener)

		#features button
		self.add_feature =  self.findChild(QtWidgets.QPushButton, 'add_feature')
		self.add_feature.clicked.connect(self.addFeatureClickListener)

		#accessories button
		self.add_accessory =  self.findChild(QtWidgets.QPushButton, 'add_accessory')
		self.add_accessory.clicked.connect(self.addAccessoryClickListener)

		#spinners declaration
		self.max_temp_spinner =  self.findChild(QtWidgets.QDoubleSpinBox, 'max_temp_spinner')
		self.min_temp_spinner =  self.findChild(QtWidgets.QDoubleSpinBox, 'min_temp_spinner')
		self.spinner_door =  self.findChild(QtWidgets.QSpinBox, 'spinner_door')


		#combo boxes declatation
		self.combo_features =  self.findChild(QtWidgets.QComboBox, 'combo_features')
		self.combo_size =  self.findChild(QtWidgets.QComboBox, 'combo_size')
		self.combo_accessories =  self.findChild(QtWidgets.QComboBox, 'combo_accessories')

		#list view declaration with its model
		self.reco_results = self.findChild(QtWidgets.QListView, 'reco_results')
		self.reco_results_model = QtGui.QStandardItemModel()
		self.reco_results.setModel(self.reco_results_model)

		#list view declaration with its model
		self.facts_list = self.findChild(QtWidgets.QListView, 'facts_list')
		self.facts_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		self.facts_list_model = QtGui.QStandardItemModel()
		self.facts_list.setModel(self.facts_list_model)

		############# Tables
		#recommendation table
		self.shop_results = self.findChild(QtWidgets.QTableView, 'shop_results')
		self.shop_results_model = QtGui.QStandardItemModel()
		self.shop_results_model.setHorizontalHeaderLabels(['Name', 'price'])
		self.shop_results.setModel(self.shop_results_model)

		#cart table
		self.cart = self.findChild(QtWidgets.QTableView, 'cart')

		#sliders and their labels
		#min price
		self.min_price = self.findChild(QtWidgets.QSlider, 'min_price')
		self.min_price_label = self.findChild(QtWidgets.QLabel, 'min_price_label')
		self.min_price.setRange(0,200000)
		self.min_price.valueChanged.connect(self.updateMinLabel)

		#max price
		self.max_price = self.findChild(QtWidgets.QSlider, 'max_price')
		self.max_price_label = self.findChild(QtWidgets.QLabel, 'max_price_label')
		self.max_price.setRange(0,1000000)
		self.max_price.valueChanged.connect(self.updateMaxLabel)

		#action buttons
		#search facts button
		self.search_facts =  self.findChild(QtWidgets.QPushButton, 'search_facts')
		self.search_facts.clicked.connect(self.searchFactsClickListener)

		#remove from fact list button 
		self.remove_fact =  self.findChild(QtWidgets.QPushButton, 'remove_fact')
		self.remove_fact.clicked.connect(self.removeFactClickListener)

		#reset fact list button 
		self.reset_facts =  self.findChild(QtWidgets.QPushButton, 'reset_facts')
		self.reset_facts.clicked.connect(self.resetFactsClickListener)

		#add to cart button
		self.add_to_cart =  self.findChild(QtWidgets.QPushButton, 'add_to_cart')
		self.add_to_cart.clicked.connect(self.addToCartClickListener)

		#remove from cart button
		self.remove_from_cart =  self.findChild(QtWidgets.QPushButton, 'remove_from_cart')
		self.remove_from_cart.clicked.connect(self.removeFromCartClickListener)

		#purchase from cart button
		self.purchase =  self.findChild(QtWidgets.QPushButton, 'purchase')
		self.purchase.clicked.connect(self.purchaseClickListener)

		#reset cart button
		self.reset_cart =  self.findChild(QtWidgets.QPushButton, 'reset_cart')
		self.reset_cart.clicked.connect(self.resetCartClickListener)

		self.show()
	
	#button click listeners
	################################################## vehicles ###################################################
	def updateMinLabel(self, value):
		self.min_price_label.setText(str(value))
	def updateMaxLabel(self, value):
		self.max_price_label.setText(str(value))
	def addSizeClickListener(self):
		item = QtGui.QStandardItem(f'size={self.combo_size.currentText()}')
		self.facts_list_model.appendRow(item)
		
	def addDoorsClickListener(self):
		item = QtGui.QStandardItem(f'doors = {self.spinner_door.value()}')
		self.facts_list_model.appendRow(item)
		
	def addMaxTempClickListener(self):
		item = QtGui.QStandardItem(f'hi_temp = {self.max_temp_spinner.value()}')
		self.facts_list_model.appendRow(item)
	def addMinTempClickListener(self):
		item = QtGui.QStandardItem(f'lo_temp = {self.min_temp_spinner.value()}')
		self.facts_list_model.appendRow(item)
	def addMaxPriceClickListener(self):
		item = QtGui.QStandardItem(f'max_price = {self.max_price.value()}')
		self.facts_list_model.appendRow(item)
	def addFeatureClickListener(self):
		string = str(self.combo_features.currentText())
		string = string.replace(" ", "")
		string = string.lower()
		item = QtGui.QStandardItem(f'features={{"{string}":1}}')
		self.facts_list_model.appendRow(item)
	def addAccessoryClickListener(self):
		string = str(self.combo_accessories.currentText())
		item = QtGui.QStandardItem(f'accessories={string}')
		self.facts_list_model.appendRow(item)  
	def addMinPriceClickListener(self):
		item = QtGui.QStandardItem(f'min_price = {self.min_price.value()}')
		self.facts_list_model.appendRow(item)
		# if len(self.FactListVehicles.selectedIndexes()) >= 1:
		#     for items in reversed(sorted(self.FactListVehicles.selectedIndexes())):
		#         self.listModel.takeRow(items.row()) 
		
	def resetFactsClickListener(self):
		self.facts_list_model.removeRows( 0, self.facts_list_model.rowCount() )
		
	def searchFactsClickListener(self):
		# for index in range(self.listModel.rowCount()):
		#     fect = f'engine.declare(Facts({self.listModel.item(index).text()}))'
		#     exec(fect)
		# engineV.run()
		# print(engineV.facts)
		pass
	def resetCartClickListener(self):
		self.cart.removeRows( 0, self.cart.rowCount() )
		
	def removeFactClickListener(self):
		# if len(self.FactListVehicles.selectedIndexes()) >= 1:
		#     for items in reversed(sorted(self.FactListVehicles.selectedIndexes())):
		#         self.listModel.takeRow(items.row()) 
		pass
	def purchaseClickListener(self):
		pass
	def removeFromCartClickListener(self):
		# if len(self.FactListVehicles.selectedIndexes()) >= 1:
		#     for items in reversed(sorted(self.FactListVehicles.selectedIndexes())):
		#         self.listModel.takeRow(items.row()) 
		pass
	def addToCartClickListener(self):
		pass
		
		

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


