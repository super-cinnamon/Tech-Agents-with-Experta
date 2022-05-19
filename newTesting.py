import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import json
import pprint


pp = pprint.PrettyPrinter(indent=4)

global received_main
global received_aux_1


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
                        msg = await self.receive(timeout=60)
                        if msg:
                                from_aux_to_main = ""
                                print(f'received the following message: {msg.body}')
                                for element in magasin_1_dict.keys():
                                        if magasin_1_dict[element]["type"] == msg.body.lower():
                                                pp.pprint(magasin_1_dict[element])
                                                from_aux_to_main+=f'{magasin_1_dict[element]["name"]}, '
                                for element in magasin_2_dict.keys():
                                        if magasin_2_dict[element]["type"] == msg.body.lower():
                                                pp.pprint(magasin_2_dict[element])
                                                from_aux_to_main+=f'{magasin_2_dict[element]["name"]}, '
                                for element in magasin_3_dict.keys():
                                        if magasin_3_dict[element]["type"] == msg.body.lower():
                                                pp.pprint(magasin_3_dict[element])
                                                from_aux_to_main+=f'{magasin_3_dict[element]["name"]}, '
                                global received_aux_1
                                received_aux_1 = from_aux_to_main
                                time.sleep(0.5)
                                self.set_next_state("sending")
                        else:
                                print("no message received after 10 seconds")
                                      
        async def setup(self):
                fsm = self.behavior()
                fsm.add_state(name="sending", state = self.sending())
                fsm.add_state(name="waiting", state = self.waiting(), initial = True)

                fsm.add_transition(source = "sending", dest = "waiting")
                fsm.add_transition(source = "waiting", dest = "sending")
                
                self.add_behaviour(fsm)

##### data base
magasin_1 = open("magasin1.json")
magasin_2 = open("magasin2.json")
magasin_3 = open("magasin3.json")

magasin_1_dict = json.load(magasin_1)
magasin_2_dict = json.load(magasin_2)
magasin_3_dict = json.load(magasin_3)



main_agent = Main_Agents("someagent@jix.im", "techagent")
auxilary_agent = Auxilary_Agents("myagent@jix.im", "techagent")
auxilary_agent_2 = Auxilary_Agents("firstagent@jix.im", "techagent")
auxilary_agent_3 = Auxilary_Agents("secondagent@jix.im", "techagent")
future = auxilary_agent.start()
future.result()
future3 = auxilary_agent_2.start()
future3.result()
future4 = auxilary_agent_3.start()
future4.result()
print("waiting for input")
global test
test = input()
future2 = main_agent.start()
future2.result()


while main_agent.is_alive():
        try:
                time.sleep(2.5)
                print("waiting for input 2")
                test = input()
                future2 = main_agent.start()
                future2.result()           
        except KeyboardInterrupt:
                auxilary_agent.stop()
                main_agent.stop()
                break
