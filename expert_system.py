from itertools import cycle
from experta import *
import experta as experta

class Facts(Fact):
    pass

class VehicleType(KnowledgeEngine):
    @Rule(AND(Facts(wheels = 2), Facts(motor = 'no'), Facts(type = 'Cycle')))
    def Bicycle(self):
        engine.retract(1)
        engine.reset()
        print("bicycle")
    @Rule(AND(Facts(wheels = 3), Facts(motor = 'no'), Facts(type = 'Cycle')))
    def Tricycle(self):
        engine.retract(1)
        engine.reset()
        print("tricycle")
    @Rule(AND(Facts(wheels = 3), Facts(motor = 'yes'), Facts(type = 'Cycle')))
    def MotorCycle(self):
        engine.retract(1)
        engine.reset()
        print("Motorcycle")

    @Rule(AND(Facts(doors = 2), Facts(size = 'Small'), Facts(type = 'automobile')))
    def SportsCar(self):
        engine.retract(1)
        engine.reset()
        print("sportscar")
    @Rule(AND(Facts(doors = 4), Facts(size = 'Medium'), Facts(type = 'automobile')))
    def Sedan(self):
        engine.retract(1)
        engine.reset()
        print("Sedan")
    @Rule(AND(Facts(doors = 3), Facts(size = 'Medium'), Facts(type = 'automobile')))
    def Minivan(self):
        engine.retract(1)
        engine.reset()
        print("Minivan")
    @Rule(AND(Facts(doors = 4), Facts(size = 'Large'), Facts(type = 'automobile')))
    def SUV(self):
        engine.retract(1)
        engine.reset()
        print("SUV")
    
    @Rule(Facts(wheels = P(lambda nb: nb < 4)))
    def Cycle(self):
        engine.duplicate(engine.facts[1], type = 'Cycle')
    @Rule(AND(Facts(wheels = 4), Facts(motor = 'yes')))
    def Auto(self):
        engine.duplicate(engine.facts[1], type = 'automobile')

#our own system
class Symptoms(Fact):
    pass
#rules to add and fill up
class Diagnosis(KnowledgeEngine):
    @Rule()
    def Arthritis(self):
        pass
    @Rule()
    def Lupus(self):
        pass
    @Rule()
    def Diarrhoea(self):
        pass
    @Rule()
    def Crohns(self):
        pass
    @Rule()
    def Anxiety(self):
        pass
    @Rule()
    def Spesis(self):
        pass
    @Rule()
    def SepticShock(self):
        pass
    @Rule()
    def ChestInfection(self):
        pass
    @Rule()
    def Bronchitis(self):
        pass
    @Rule()
    def Pneumonia(self):
        pass
    @Rule()
    def Asthma(self):
        pass
    @Rule()
    def AsthmaAttack(self):
        pass
    @Rule()
    def CommonCold(self):
        pass
    @Rule()
    def Flu(self):
        pass
    @Rule()
    def EColi(self):
        pass
    @Rule()
    def Covid19(self):
        pass
    @Rule()
    def Tonsilis(self):
        pass
    @Rule()
    def HayFever(self):
        pass
    @Rule()
    def heartFailure(self):
        pass
    @Rule()
    def Amaemia(self):
        pass
    @Rule()
    def Ulcer(self):
        pass
    @Rule()
    def HIV(self):
        pass
    @Rule()
    def KidneyInfection(self):
        pass
    @Rule()
    def KidneyStones(self):
        pass
    @Rule()
    def LiverDisease(self):
        pass
    @Rule()
    def Measles(self):
        pass
    @Rule()
    def Migraine(self):
        pass

engine =  VehicleType()
engine.reset()
engine.declare(Facts(wheels = 4, motor = 'yes', size = 'Medium', doors = 4))
engine.run()
