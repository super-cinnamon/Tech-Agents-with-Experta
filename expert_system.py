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
        print("sportscar")
    @Rule(AND(Facts(doors = 3), Facts(size = 'Medium'), Facts(type = 'automobile')))
    def Minivan(self):
        engine.retract(1)
        engine.reset()
        print("sportscar")
    @Rule(AND(Facts(doors = 4), Facts(size = 'Large'), Facts(type = 'automobile')))
    def SUV(self):
        engine.retract(1)
        engine.reset()
        print("sportscar")
    
    @Rule(Facts(wheels = P(lambda nb: nb < 4)))
    def Cycle(self):
        engine.duplicate(engine.facts[1], type = 'Cycle')
    @Rule(AND(Facts(wheels = 4), Facts(motor = 'yes')))
    def Auto(self):
        engine.duplicate(engine.facts[1], type = 'automobile')



engine =  VehicleType()
engine.reset()
engine.declare(Facts(wheels = 3, motor = 'yes'))
engine.run()
