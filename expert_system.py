from itertools import cycle
from experta import *
import experta as experta
from sympy import sympify

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
        #engine.retract(1)
        print("fever")

engine =  Diagnosis()
engine.reset()
engine.declare(Symptoms(temperature = 37.0))
engine.declare(Symptoms(joint_pain = True))
engine.declare(Symptoms(fatigue = True))
engine.declare(Symptoms(rashes = True))
engine.run()
print(engine.facts)

