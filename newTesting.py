import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour, FMSBehaviour, State
from spade.message import Message
from spade.template import Template

class Main_Agents(Agent):
        def set_message(self, message):
                self.message = message
        class behavior(FMSBehaviour):
                pass
        class sending(State):
                def get_message(self, message):
                        self.message = message
                pass
        class waiting(State):
                pass
        async def setup(self):
                fms = self.behavior()

class Auxilary_Agents(Agent):
        pass
