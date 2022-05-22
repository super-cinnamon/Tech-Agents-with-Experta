from cgi import test
from unicodedata import name
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
###################################   test with the expert system
from itertools import cycle
from experta import *
import experta as experta


import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import json


global received_main
global received_aux_1
received_aux_1 = ""

magasin_1 = open("magasin1.json","r+")
magasin_2 = open("magasin2.json","r+")
magasin_3 = open("magasin3.json","r+")

magasin_1_dict = json.load(magasin_1)
magasin_2_dict = json.load(magasin_2)
magasin_3_dict = json.load(magasin_3)


getFridges = []
fridge_features = []
additional_features = []
invocated_rules = []

class Facts(Fact):
	pass

class myEngine(KnowledgeEngine):
################################################################################################################################
################################################# fridge rules ########################################################
	@Rule(Facts(doors = P(lambda nb: nb <= 3)))
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
	@Rule(Facts(size = 'Small'), Facts(doors = 1), Facts(has_freezer = False))
	def MiniFridge(self):
		getFridges.append("Mini Fridge")
	@Rule(Facts(size = 'Large'), Facts(doors = 2), Facts(has_freezer = True))
	def SideBySide(self):
		getFridges.append("Side-By-Side Fridge")
	@Rule(Facts(size = 'Large'), Facts(french_fridge = True), Facts(has_freezer = True))
	def FrenchDoorFridge(self):
		getFridges.append("French Doors Fridge")
	@Rule(Facts(size = 'Medium'), Facts(doors = 2), Facts(has_freezer = True))
	def StandardFridge(self):
		getFridges.append("Standard Fridge")
	@Rule(Facts(size = 'Medium'), Facts(doors = 1), Facts(has_freezer = False))
	def SimpleFridge(self):
		getFridges.append("Simple Fridge")
	@Rule(Facts(size = 'Large'),Facts(french_fridge = True), Facts(features__tablet =  1), Facts(has_freezer = True))
	def SmartFridge(self):
		getFridges.append("Smart Fridge")
	@Rule(Facts(size = 'Extra Large'), Facts(has_freezer = False), Facts(doors = 2))
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
engineV.reset()
		
#################################################################################################################################
############################################### G U I ###########################################################################
class Second(QtWidgets.QDialog):
	def __init__(self):
		super(Second, self).__init__()
		uic.loadUi('receipt.ui', self)
		global receipt
		global receipt_model
		self.receipt = self.findChild(QtWidgets.QTableView, 'receipt')		
		self.receipt_model = QtGui.QStandardItemModel()
		self.receipt_model.setHorizontalHeaderLabels(['ID', 'Name', 'color', 'price', 'quantity','shop'])
		self.receipt.setModel(self.receipt_model)
		receipt=self.receipt
		receipt_model=self.receipt_model

		self.buy =  self.findChild(QtWidgets.QPushButton, 'validate_purchase')
		self.buy.clicked.connect(self.buyClickListener)

		self.cancel_purchase =  self.findChild(QtWidgets.QPushButton, 'cancel_purchase')
		self.cancel_purchase.clicked.connect(self.cancelClickListener)

		global total
		self.total =  self.findChild(QtWidgets.QPlainTextEdit, 'total')
		total=self.total
		total.setReadOnly(True)

	def buyClickListener(self):
		items=[]
		for row in range(receipt_model.rowCount(receipt.rootIndex())):
			items.append(receipt_model.index(row, 0, receipt.rootIndex())) # for column 0
		rows = sorted(set(index.row() for index in items))
		for row in rows:
			id=receipt.model().data(receipt.model().index(row, 0))
			numeroMagasin=receipt.model().data(receipt.model().index(row, 5))
			print('id : ',id,' numero du magasin : ',numeroMagasin)
			if(numeroMagasin=='1'):
				produit=magasin_1_dict[id]
				produit['number in stock']-=1
				updt=json.dumps(magasin_1_dict, indent=4)
				magasin_1.write(updt)
			if(numeroMagasin=='2'):
				produit=magasin_2_dict[id]
				produit['number in stock']-=1
				updt=json.dumps(magasin_2_dict, indent=4)
				magasin_2.write(updt)
			if(numeroMagasin=='3'):
				produit=magasin_3_dict[id]
				produit['number in stock']-=1
				updt=json.dumps(magasin_3_dict, indent=4)
				magasin_3.write(updt)
		print("achat effectué avec succès")
		self.close()

	def cancelClickListener(self):
		self.close()

	def fillTable(self):
		items = []
		prixTotal=0
		for row in range(cart_purchase.rowCount(cart.rootIndex())):
			items.append(cart_purchase.index(row, 0, cart.rootIndex())) # for column 0
		rows = sorted(set(index.row() for index in items))
		for row in rows:
			produit=[]
			idIndex=cart.model().index(row, 0)
			nameIndex = cart.model().index(row, 1)
			priceIndex=cart.model().index(row, 3)
			id=cart.model().data(idIndex)
			Name = cart.model().data(nameIndex)
			price=cart.model().data(priceIndex)
			prixTotal=prixTotal+int(price)
			print('name is ',Name,' price is ',price,' prix total: ',prixTotal)
			produit.append(id)
			produit.append(Name)
			produit.append(cart.model().data(cart.model().index(row,2)))
			produit.append(price)
			produit.append(cart.model().data(cart.model().index(row,4)))
			produit.append(cart.model().data(cart.model().index(row,5)))
			selectedProducts=[]
			for element in produit:
				selectedProducts.append(QtGui.QStandardItem(element))
			self.receipt_model.appendRow(selectedProducts)
			self.total.setPlainText(str(prixTotal))

		

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
		global shop_res
		self.shop_results = self.findChild(QtWidgets.QTableView, 'shop_results')
		self.shop_results_model = QtGui.QStandardItemModel()
		global shop
		self.shop_results_model.setHorizontalHeaderLabels(['ID', 'Name', 'color', 'price', 'quantity','shop'])
		self.shop_results.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		self.shop_results.setModel(self.shop_results_model)
		shop = self.shop_results_model
		shop_res = self.shop_results

		#cart table
		global cart_purchase
		global cart
		self.cart = self.findChild(QtWidgets.QTableView, 'cart')
		self.cart_model = QtGui.QStandardItemModel()
		self.cart_model.setHorizontalHeaderLabels(['ID', 'Name', 'color', 'price', 'quantity','shop'])
		self.cart.setModel(self.cart_model)
		cart_purchase = self.cart_model
		cart = self.cart

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
		self.shop_results_model.removeRows(0, self.shop_results_model.rowCount() )

		for index in range(self.facts_list_model.rowCount()):
			item = self.facts_list_model.item(index).text()
			if "price" not in item and "accessories" not in item:
				if "size" in item:
					equals = item.index("=")
					item = f'{item[:equals+1]}\'{item[equals+1:].strip()}\''
				fect = f'engineV.declare(Facts({item}))'
				exec(fect)
			if "accessories" in item:
				additional_features.append(item[item.index("=")+1:])

		engineV.run()
		engineV.reset()
		self.reco_results_model.removeRows( 0, self.reco_results_model.rowCount() )
		for element in getFridges:
			item = QtGui.QStandardItem(f'{element}')
			self.reco_results_model.appendRow(item)
		if(getFridges and fridge_features):
			self.reco_results_model.appendRow(QtGui.QStandardItem(f'with features'))
			for element in fridge_features:
				self.reco_results_model.appendRow( QtGui.QStandardItem(f'{element}'))
		
		fridge_features.clear()

		global test
		test = ', '.join(getFridges)
		test = test.lower()
		getFridges.clear()  #clear at the end

		################### here will be the agents to fill the shop table
		global future4
		future4.result()
		
		future2 = main_agent.start()
		future2.result()
		
	def resetCartClickListener(self):
		self.cart_model.removeRows( 0, self.cart_model.rowCount() )
		
	def removeFactClickListener(self):
		if len(self.facts_list.selectedIndexes()) >= 1:
			for items in reversed(sorted(self.facts_list.selectedIndexes())):
				self.facts_list_model.takeRow(items.row()) 
		
	def purchaseClickListener(self):
		self.receipt = Second()
		self.receipt.fillTable()
		self.receipt.show()
	def removeFromCartClickListener(self):
		if len(self.cart.selectedIndexes()) >= 1:
			for items in reversed(sorted(self.cart.selectedIndexes())):
				self.cart_model.takeRow(items.row()) 
	def addToCartClickListener(self):
		if len(self.shop_results.selectedIndexes()) >= 1:
			
			rows = sorted(set(index.row() for index in self.shop_results.selectedIndexes()))
			for row in rows:
				produit=[]
				print('Row %d is selected' % row)
				idIndex=self.shop_results.model().index(row, 0)
				nameIndex = self.shop_results.model().index(row, 1)
				priceIndex=self.shop_results.model().index(row, 3)
				id=self.shop_results.model().data(idIndex)
				Name = self.shop_results.model().data(nameIndex)
				price=self.shop_results.model().data(priceIndex)
				print('name is ',Name,' price is ',price)
				produit.append(id)
				produit.append(Name)
				#color
				produit.append(self.shop_results.model().data(self.shop_results.model().index(row,2)))
				produit.append(price)
				#quantity
				produit.append(self.shop_results.model().data(self.shop_results.model().index(row,4)))
				produit.append(self.shop_results.model().data(self.shop_results.model().index(row,5)))
				selectedProducts=[]
				for element in produit:
					selectedProducts.append(QtGui.QStandardItem(element))
				self.cart_model.appendRow(selectedProducts)
		
##############################################################################################################################
################################ AGENTS


	class Main_Agents(Agent):
		class behavior(FSMBehaviour):
			async def on_start(self):
				print("behavior main started")
			async def on_end(self):
				print("behavior main ended")
		class sending(State):
			async def run(self):
				msg = Message(to="myagent@jix.im")
				msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
				global test
				msg.body = f'{test}'
				await self.send(msg)
				print("message sent")
				global received_aux_1
				received_aux_1=""
				time.sleep(0.5)
				self.set_next_state("waiting")
		class waiting(State):
			async def run(self):
				msg = await self.receive(timeout=60)
				if msg:
					global received_main
					received_main = msg
					print(f'received the following message: {msg.body}')
					time.sleep(0.5)
					results = msg.body.split(", ")
					for each in results:
						current = each.split("; ")
						row = []
						for element in current:
							if element != "":
								row.append(QtGui.QStandardItem(element))
						shop.appendRow(row)
					shop.removeRow(shop.rowCount()-1)
					self.set_next_state("final_state")
				else:
					print("no message received after 10 seconds")
		class final_state(State):
			async def run(self):
				print("main agent is done!")
				self.kill()
					
		async def setup(self):
			fsm = self.behavior()
			fsm.add_state(name="sending", state = self.sending(), initial = True)
			fsm.add_state(name="waiting", state = self.waiting())
			fsm.add_state(name="final_state", state = self.final_state())

			fsm.add_transition(source = "sending", dest = "waiting")
			fsm.add_transition(source = "waiting", dest = "sending")
			fsm.add_transition(source = "waiting", dest = "final_state")

			self.add_behaviour(fsm)


	class Auxilary_Agents(Agent):
		class behavior(FSMBehaviour):
			async def on_start(self):
				print("behavior aux started")
			async def on_end(self):
				print("behavior aux ended")
		class sending(State):
			async def run(self):
				msg = Message(to="someagent@jix.im")
				msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
				print(f'aux is sending {received_aux_1}')
				msg.body = f'{received_aux_1}'
				await self.send(msg)
				print("message sent")
				time.sleep(0.5)
				self.set_next_state("waiting")
		class waiting(State):
			async def run(self):
				msg = await self.receive(timeout=999)
				if msg:
					from_aux_to_main = ""
					print(f'received the following message: {msg.body}')
					for element in magasin_1_dict.keys():
						if magasin_1_dict[element]["type"] == msg.body.lower():
							from_aux_to_main+=f'{element}; {magasin_1_dict[element]["name"]}; {magasin_1_dict[element]["color"]}; {magasin_1_dict[element]["price"]}; {magasin_1_dict[element]["number in stock"]}; 1, '
					for element in magasin_2_dict.keys():
						if magasin_2_dict[element]["type"] == msg.body.lower():
							from_aux_to_main+=f'{element}; {magasin_2_dict[element]["name"]}; {magasin_2_dict[element]["color"]}; {magasin_2_dict[element]["price"]}; {magasin_2_dict[element]["number in stock"]}; 2, '
					for element in magasin_3_dict.keys():
						if magasin_3_dict[element]["type"] == msg.body.lower():
							from_aux_to_main+=f'{element}; {magasin_3_dict[element]["name"]}; {magasin_3_dict[element]["color"]}; {magasin_3_dict[element]["price"]}; {magasin_3_dict[element]["number in stock"]}; 3, '
					for each in additional_features:
						for element in magasin_1_dict.keys():
							if magasin_1_dict[element]["type"] == each.lower():
								from_aux_to_main+=f'{element}; {magasin_1_dict[element]["name"]}; {magasin_1_dict[element]["color"]}; {magasin_1_dict[element]["price"]}; {magasin_1_dict[element]["number in stock"]}; 1, '
						for element in magasin_2_dict.keys():
							if magasin_2_dict[element]["type"] == each.lower():
								from_aux_to_main+=f'{element}; {magasin_2_dict[element]["name"]}; {magasin_2_dict[element]["color"]}; {magasin_2_dict[element]["price"]}; {magasin_2_dict[element]["number in stock"]}; 2, '
						for element in magasin_3_dict.keys():
							if magasin_3_dict[element]["type"] == each.lower():
								from_aux_to_main+=f'{element}; {magasin_3_dict[element]["name"]}; {magasin_3_dict[element]["color"]}; {magasin_3_dict[element]["price"]}; {magasin_3_dict[element]["number in stock"]}; 3, '
					global received_aux_1
					received_aux_1 = from_aux_to_main
					time.sleep(0.5)
					self.set_next_state("sending")
				else:
					print("no message received after 999 seconds")
					
		async def setup(self):
			fsm = self.behavior()
			fsm.add_state(name="sending", state = self.sending())
			fsm.add_state(name="waiting", state = self.waiting(), initial = True)

			fsm.add_transition(source = "sending", dest = "waiting")
			fsm.add_transition(source = "waiting", dest = "sending")
			
			self.add_behaviour(fsm)

	##### data base
	
	global main_agent
	main_agent = Main_Agents("someagent@jix.im", "techagent")
	global auxilary_agent
	auxilary_agent = Auxilary_Agents("myagent@jix.im", "techagent")
	global auxilary_agent_2
	auxilary_agent_2 = Auxilary_Agents("firstagent@jix.im", "techagent")
	global auxilary_agent_3
	auxilary_agent_3 = Auxilary_Agents("secondagent@jix.im", "techagent")

	
	future = auxilary_agent.start()
	future.result()
	future3 = auxilary_agent_2.start()
	future3.result()
	global future4
	future4 = auxilary_agent_3.start()

			

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


