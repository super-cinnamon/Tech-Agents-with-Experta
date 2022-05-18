import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

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
                        msg.body = "this is the main agent"
                        await self.send(msg)
                        print("message sent")
                        time.sleep(0.5)
                        self.set_next_state("waiting")
        class waiting(State):
                async def run(self):
                        msg = await self.receive(timeout=10)
                        if msg:
                                global received_main
                                received_main = msg
                                print(f'received the following message: {msg.body}')
                                time.sleep(0.5)
                                self.set_next_state("sending")
                        else:
                                print("no message received after 10 seconds")
                        
                
        async def setup(self):
                fsm = self.behavior()
                fsm.add_state(name="sending", state = self.sending(), initial = True)
                fsm.add_state(name="waiting", state = self.waiting())

                fsm.add_transition(source = "sending", dest = "waiting")
                fsm.add_transition(source = "waiting", dest = "sending")

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
                        msg.body = f'the received message was: {received_aux_1.body}'
                        await self.send(msg)
                        print("message sent")
                        time.sleep(0.5)
                        self.set_next_state("waiting")
        class waiting(State):
                async def run(self):
                        msg = await self.receive(timeout=10)
                        if msg:
                                global received_aux_1
                                received_aux_1 = msg
                                print(f'received the following message: {msg.body}')
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

main_agent = Main_Agents("someagent@jix.im", "techagent")
auxilary_agent = Auxilary_Agents("myagent@jix.im", "techagent")
future = auxilary_agent.start()
future.result()
future2 = main_agent.start()
future2.result()

while main_agent.is_alive():
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            auxilary_agent.stop()
            main_agent.stop()
            break
