from itertools import cycle
from experta import *
import experta as experta

getFridges = []
getVehicle = []
getDiagnosis = []

class Facts(Fact):
	pass

class myEngine(KnowledgeEngine):
	@Rule(AND(Facts(wheels = 2), Facts(motor = 'no'), Facts(type = 'Cycle')))
	def Bicycle(self):
		engineV.retract(1)
		getVehicle.append("Bicycle")
		engineV.reset()
	@Rule(AND(Facts(wheels = 3), Facts(motor = 'no'), Facts(type = 'Cycle')))
	def Tricycle(self):
		engineV.retract(1)
		getVehicle.append("Tricycle")
		engineV.reset()
	@Rule(AND(Facts(wheels = 3), Facts(motor = 'yes'), Facts(type = 'Cycle')))
	def MotorCycle(self):
		engineV.retract(1)
		getVehicle.append("Motorcycle")
		engineV.reset()

	@Rule(AND(Facts(doors = 2), Facts(size = 'Small'), Facts(type = 'automobile')))
	def SportsCar(self):
		engineV.retract(1)
		getVehicle.append("Sports Car")
		engineV.reset()
	@Rule(AND(Facts(doors = 4), Facts(size = 'Medium'), Facts(type = 'automobile')))
	def Sedan(self):
		engineV.retract(1)
		getVehicle.append("Sedan")
		engineV.reset()
	@Rule(AND(Facts(doors = 3), Facts(size = 'Medium'), Facts(type = 'automobile')))
	def Minivan(self):
		engineV.retract(1)
		getVehicle.append("Minivan")
		engineV.reset()
	@Rule(AND(Facts(doors = 4), Facts(size = 'Large'), Facts(type = 'automobile')))
	def SUV(self):
		engineV.retract(1)
		getVehicle.append("SUV")
		engineV.reset()
	
	@Rule(Facts(wheels = P(lambda nb: nb < 4)))
	def Cycle(self):
		engineV.duplicate(engineV.facts[1], type = 'Cycle')
	@Rule(AND(Facts(wheels = 4), Facts(motor = 'yes')))
	def Auto(self):
		engineV.duplicate(engineV.facts[1], type = 'automobile')
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
	@Rule(Facts(french_fridge = True), Facts(has_freezer = True))
	def FrenchDoorFridge(self):
		getFridges.append("French Doors Fridge")
	@Rule(Facts(size = 'Medium'), Facts(f_doors = 2), Facts(has_freezer = True))
	def StandardFridge(self):
		getFridges.append("Standard Fridge")
	@Rule(Facts(size = 'Medium'), Facts(f_doors = 1), Facts(has_freezer = False))
	def SimpleFridge(self):
		getFridges.append("Simple Fridge")
	@Rule(Facts(french_fridge = True), Facts(features__tablet =  1))
	def SmartFridge(self):
		getFridges.append("Smart Fridge")
	@Rule(Facts(size = 'Extra Large'), Facts(has_freezer = False), Facts(f_doors = 2))
	def ColumnFridge(self):
		getFridges.append("Column Fridge")
	@Rule(Facts(features__waterdispenser = 1))
	def FeatureWater(self):
		pass
	@Rule(Facts(features__icedispenser = 1))
	def FeatureIce(self):
		pass
		


#our medical diagnosis system (in a separate engine)
class Symptoms(Fact):
	pass
#rules to add and fill up
class Diagnosis(KnowledgeEngine):
	@Rule(Symptoms(joint_pain = True))
	def Arthritis(self):
		engine.declare(Symptoms(arthritis = True))
		print("arthritis")
	@Rule(Symptoms(arthritis = True), Symptoms(fatigue = True), Symptoms(rashes = True))
	def Lupus(self):
		print("lupus")
	@Rule(Symptoms(stomachache = True), Symptoms(nausea = True), Symptoms(headache = True), Symptoms(appetite_loss = True), Symptoms(vomiting = True))
	def Diarrhoea(self):
		engine.declare(Symptoms(diarrhoea = True))
		print("diarrhoea")
	@Rule(Symptoms(diarrhoea = True), Symptoms(fatigue = True), Symptoms(weight_loss = True), Symptoms(bloodied_feces = True))
	def Crohns(self):
		print("crohn's disease")
	@Rule(Symptoms(diziness = True), Symptoms(fatigue = True), Symptoms(shortness_of_breath = True), Symptoms(trembeling_or_shaking = True), Symptoms(headache = True), Symptoms(muscle_aches = True), Symptoms(palpitations = True), Symptoms(stomachaches = True), Symptoms(insomnia = True), Symptoms(excessive_sweating = True))
	def Anxiety(self):
		print("anxiety")
	@Rule(Symptoms(paleness = True), Symptoms(fast_breathing = True), Symptoms(rashes = True))
	def Sepsis(self):
		engine.declare(Symptoms(sepsis = True))
		print("sepsis")
	@Rule(Symptoms(diziness = True), Symptoms(diarrhoea = True), Symptoms(nausea = True), Symptoms(sepsis = True), Symptoms(vomiting = True), Symptoms(confusion = True))
	def SepticShock(self):
		print("septic shock")
	@Rule(Symptoms(coughing = True), Symptoms(shortness_of_breath = True), Symptoms(fever = True), Symptoms(palpitations = True), Symptoms(chest_pain = True), Symptoms(confusion = True))
	def ChestInfection(self):
		engine.declare(Symptoms(chest_infection = True))
		print("chest infection")
	@Rule(Symptoms(sore_throat = True), Symptoms(headache = True), Symptoms(runny_nose = True), Symptoms(general_aches = True), Symptoms(fatigue = True), Symptoms(chest_infection = True))
	def Bronchitis(self):
		print("brochitis")
	@Rule(Symptoms(chest_infection = True), Symptoms(excessive_sweating = True), Symptoms(appetite_loss = True), Symptoms(trembeling_or_shaking = True))
	def Pneumonia(self):
		print("pneumonia")
	@Rule(Symptoms(shortness_of_breath = True), Symptoms(coughing = True), Symptoms(chest_pain = True))
	def Asthma(self):
		engine.declare(Symptoms(asthma = True))
		print("asthma")
	@Rule(Symptoms(asthma = True), Symptoms(fatigue = True), Symptoms(palpitations = True), Symptoms(diziness = True), Symptoms(cyanosis = True), Symptoms(fast_breathing = True))
	def AsthmaAttack(self):
		print("asthma attack")
	@Rule(Symptoms(sore_throat = True), Symptoms(runny_nose = True), Symptoms(sneezing = True), Symptoms(coughing = True))
	def CommonCold(self):
		print("common cold")
	@Rule(Symptoms(fever = True), Symptoms(cough = True), Symptoms(muscle_pain = True), Symptoms(joint_pain = True), Symptoms(fatigue = True), Symptoms(headache = True), OR(Symptoms(diarroea = True), Symptoms(stomachache = True)), OR(Symptoms(nausea = True), Symptoms(vomiting = True)), Symptoms(sore_throat = True), Symptoms(sneezing = True), Symptoms(appetite_loss = True), Symptoms(insomnia = True))
	def Flu(self):
		print("flu")
	@Rule(Symptoms(diarrhoea = True), Symptoms(fever = True), Symptoms(bloodied_feces = True))
	def EColi(self):
		print("e coli")
	@Rule(Symptoms(fever = True), Symptoms(cough = True), Symptoms(Fatigue = True), Symptoms(sore_throat = True), Symptoms(general_aches = True))
	def Covid19(self):
		print("covid 19")
	@Rule(Symptoms(cough = True), Symptoms(headache = True), Symptoms(earache = True), Symptoms(fatigue = True))
	def Tonsilitis(self):
		print("tonsilitis")
	@Rule(Symptoms(sneezing = True), Symptoms(runny_nose = True), Symptoms(itching = True), Symptoms(eye_inflamation_or_irritation = True), Symptoms(coughing = True))
	def HayFever(self):
		print("hay faver")
	@Rule(Symptoms(shortness_of_breath = True), Symptoms(fatigue = True), Symptoms(swollen_skin = True), Symptoms(appetite_loss = True))
	def heartFailure(self):
		print("heart failure")
	@Rule(Symptoms(fatigue = True), Symptoms(shortness_of_breath = True), Symptoms(palpitations = True), Symptoms(paleness = True))
	def Anaemia(self):
		print("anaemia")
	@Rule(Symptoms(stomachache = True), Symptoms(appetite_loss = True), Symptoms(weight_loss = True))
	def Ulcer(self):
		print("ulcer")
	@Rule(Symptoms(fever = True), Symptoms(sore_throat = True), Symptoms(rashes = True), Symptoms(fatigue = True), Symptoms(joint_pain = True), Symptoms(muscle_pain = True), Symptoms(weight_loss = True), Symptoms(diarrhoea = True), Symptoms(excessive_sweating = True))
	def HIV(self):
		print("HIV")
	@Rule(Symptoms(lower_back_pain = True), Symptoms(fever = True), Symptoms(trembling_or_shaking = True), Symptoms(fatigue = True), Symptoms(appetite_loss = True), Symptoms(diarrhoea = True))
	def KidneyInfection(self):
		print("kidney infection")
	@Rule(Symptoms(kidney_infection = True), Symptoms(nausea = True))
	def KidneyStones(self):
		print("kidney stones")
	@Rule(Symptoms(runny_nose = True), Symptoms(sneezing = True), Symptoms(coughing = True), Symptoms(general_aches = True), Symptoms(appetite_loss = True), Symptoms(eye_inflamation_or_irritation = True), Symptoms(fever = True), Symptoms(fatigue = True))
	def Measles(self):
		print("measles")
	@Rule(Symptoms(nausea = True), Symptoms(headache = True))
	def Migraine(self):
		print("migraine")
	@Rule(Symptoms(temperature = P(lambda nb: nb >= 37.0)))
	def Fever(self):
		engine.declare(Symptoms(fever = True))
		print("fever")


engine =  Diagnosis()
engine.reset()
engine.declare(Symptoms(temperature = 37.0))
engine.declare(Symptoms(joint_pain = True))
engine.declare(Symptoms(fatigue = True))
engine.declare(Symptoms(rashes = True))
#engine.run()

########################################################################################################################################################################
##############################################                 G U I               #####################################################################################

from PyQt5 import QtWidgets, uic, QtGui
import sys


engineV =  myEngine()
engineV.reset()


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

		#get vehicle button
		self.getVehicle =  self.findChild(QtWidgets.QPushButton, 'getVehicle')
		self.getVehicle.clicked.connect(self.getVehicleClickListener)

		#fact list view declaration with its model
		self.FactListVehicles = self.findChild(QtWidgets.QListView, 'listView')
		self.FactListVehicles.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		self.listModel = QtGui.QStandardItemModel()
		self.FactListVehicles.setModel(self.listModel)

		#vehicle result declaration
		self.Vehicle = self.findChild(QtWidgets.QListView, 'vehicle')
		self.vehicleModel = QtGui.QStandardItemModel()
		self.Vehicle.setModel(self.vehicleModel)

		#remove from fact list button 
		self.removeVehicleFact =  self.findChild(QtWidgets.QPushButton, 'removeVehicleFact')
		self.removeVehicleFact.clicked.connect(self.removeVehicleFactClickListener)
		#reset fact list button 
		self.resetFacts =  self.findChild(QtWidgets.QPushButton, 'resetFacts')
		self.resetFacts.clicked.connect(self.resetFactsClickListener)

		####################################### fridge items ########################################
		#spinners for temperature and number of doors
		self.loTemp =  self.findChild(QtWidgets.QDoubleSpinBox, 'lo_temp')
		self.hiTemp =  self.findChild(QtWidgets.QDoubleSpinBox, 'hi_temp')
		self.fDoors =  self.findChild(QtWidgets.QSpinBox, 'f_doors')
		
		#size combo box
		self.fSize =  self.findChild(QtWidgets.QComboBox, 'f_size')
		self.addFeature =  self.findChild(QtWidgets.QComboBox, 'add_feature')

		#list views and their models
		#fact list view declaration with its model
		self.FactListFridge = self.findChild(QtWidgets.QListView, 'fridgeFacts')
		self.FactListFridge.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		self.fridgeModel = QtGui.QStandardItemModel()
		self.FactListFridge.setModel(self.fridgeModel)

		#vehicle result declaration
		self.Fridges = self.findChild(QtWidgets.QListView, 'fridges')
		self.resultsFridgeModel = QtGui.QStandardItemModel()
		self.Fridges.setModel(self.resultsFridgeModel)

		#buttons declaration
		#add doors
		self.addFdoors =  self.findChild(QtWidgets.QPushButton, 'addFdoors')
		self.addFdoors.clicked.connect(self.getFDoorsClickListener)
		#add size
		self.addFridgeSize =  self.findChild(QtWidgets.QPushButton, 'addFsize')
		self.addFridgeSize.clicked.connect(self.getFSizeClickListener)
		#add low temp
		self.addLoTemp =  self.findChild(QtWidgets.QPushButton, 'addLoTemp')
		self.addLoTemp.clicked.connect(self.getLoTempClickListener)
		#add high temp
		self.addHiTemp =  self.findChild(QtWidgets.QPushButton, 'addHiTemp')
		self.addHiTemp.clicked.connect(self.getHiTempClickListener)
		#add additional feature
		self.addFeatures =  self.findChild(QtWidgets.QPushButton, 'addFeatures')
		self.addFeatures.clicked.connect(self.getFeaturesClickListener)
		#remove from fact list
		self.removeFFact =  self.findChild(QtWidgets.QPushButton, 'removeFridgeFact')
		self.removeFFact.clicked.connect(self.removeFactClickListener)
		#get fridge result
		self.getFridge =  self.findChild(QtWidgets.QPushButton, 'getFridge')
		self.getFridge.clicked.connect(self.getFridgeClickListener)
		#reset fact list
		self.resetFridgeFacts =  self.findChild(QtWidgets.QPushButton, 'resetFactsFridge')
		self.resetFridgeFacts.clicked.connect(self.resetFridgeFactsClickListener)


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
		#sypmtoms list view declaration with its model
		self.FactListSymptoms = self.findChild(QtWidgets.QListView, 'symptomsList')
		self.FactListSymptoms.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		self.sympModel = QtGui.QStandardItemModel()
		self.FactListSymptoms.setModel(self.sympModel)

		#diagnosis list view declaration with its model
		self.Diagnosis = self.findChild(QtWidgets.QListView, 'diagnosis')
		self.diagnosisModel = QtGui.QStandardItemModel()
		self.Diagnosis.setModel(self.diagnosisModel)

		#remove from fact list button 
		self.removeSymptom =  self.findChild(QtWidgets.QPushButton, 'removeSymptom')
		self.removeSymptom.clicked.connect(self.removeSymptomClickListener)
		#reset fact list button 
		self.resetSymptoms =  self.findChild(QtWidgets.QPushButton, 'resetSymptoms')
		self.resetSymptoms.clicked.connect(self.resetSymptomsClickListener)
		#diagnose button
		self.diagnose =  self.findChild(QtWidgets.QPushButton, 'diagnose')
		self.diagnose.clicked.connect(self.diagnoseClickListener)
		
		self.show()
	
	#button click listeners
	################################################## vehicles ###################################################
	def getWheelsClickListener(self):
		item = QtGui.QStandardItem(f'wheels={self.wheels.value()}')
		self.listModel.appendRow(item)
	def getDoorsClickListener(self):
		item = QtGui.QStandardItem(f'doors={self.doors.value()}')
		self.listModel.appendRow(item)
	def getMotorClickListener(self):
		item = QtGui.QStandardItem(f'motor={self.motor.currentText()}')
		self.listModel.appendRow(item)
	def getSizeClickListener(self):
		item = QtGui.QStandardItem(f'size={self.size.currentText()}')
		self.listModel.appendRow(item)
	def removeVehicleFactClickListener(self):
		if len(self.FactListVehicles.selectedIndexes()) >= 1:
			for items in reversed(sorted(self.FactListVehicles.selectedIndexes())):
				self.listModel.takeRow(items.row()) 
	def resetFactsClickListener(self):
		self.listModel.removeRows( 0, self.listModel.rowCount() )
	def getVehicleClickListener(self):
		#getVehicle = [] tried to init it this way and it's just always empty..............
		for index in range(self.listModel.rowCount()):
			item = self.listModel.item(index).text()
			if "wheels" in item :
				fect = f'engineV.declare(Facts({item}))'
				exec(fect)
				break
		for index in range(self.listModel.rowCount()):
			item = self.listModel.item(index).text()
			if "wheels" not in item:
				if "motor" in item or "size" in item:
					equals = item.index("=")
					item = f'{item[:equals+1]}\'{item[equals+1:].strip()}\''
				fect = f'engineV.declare(Facts({item}))'
				exec(fect)
		engineV.run()
		engineV.reset()
		self.vehicleModel.removeRows( 0, self.vehicleModel.rowCount() )
		for element in getVehicle:
			item = QtGui.QStandardItem(f'{element}')
			self.vehicleModel.appendRow(item)
		getVehicle.clear()

	################################################# fridge ####################################################
	def getFDoorsClickListener(self):
		item = QtGui.QStandardItem(f'f_doors={self.fDoors.value()}')
		self.fridgeModel.appendRow(item)
	def getFSizeClickListener(self):
		item = QtGui.QStandardItem(f'size={self.fSize.currentText()}')
		self.fridgeModel.appendRow(item)
	def getLoTempClickListener(self):
		item = QtGui.QStandardItem(f'lo_temp={self.loTemp.value()}')
		self.fridgeModel.appendRow(item)
	def getHiTempClickListener(self):
		item = QtGui.QStandardItem(f'hi_temp={self.hiTemp.value()}')
		self.fridgeModel.appendRow(item)
	def getFeaturesClickListener(self):
		string = str(self.addFeature.currentText())
		string = string.strip()
		string = string.lower()
		item = QtGui.QStandardItem(f'features__{string}=1')
		self.fridgeModel.appendRow(item)
	def removeFactClickListener(self):
		if len(self.FactListFridge.selectedIndexes()) >= 1:
			for items in reversed(sorted(self.FactListFridge.selectedIndexes())):
				self.fridgeModel.takeRow(items.row()) 
	def getFridgeClickListener(self):
		print("test")
		for index in range(self.fridgeModel.rowCount()):
			item = self.fridgeModel.item(index).text()
			if "size" in item:
				equals = item.index("=")
				item = f'{item[:equals+1]}\'{item[equals+1:].strip()}\''
			fect = f'engineV.declare(Facts({item}))'
			print(fect)
			exec(fect)
		engineV.run()
		engineV.reset()
		self.resultsFridgeModel.removeRows( 0, self.resultsFridgeModel.rowCount() )
		for element in getFridges:
			item = QtGui.QStandardItem(f'{element}')
			self.resultsFridgeModel.appendRow(item)
		getFridges.clear()
	def resetFridgeFactsClickListener(self):
		self.fridgeModel.removeRows( 0, self.fridgeModel.rowCount())
	
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
	def diagnoseClickListener(self):
		pass

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


