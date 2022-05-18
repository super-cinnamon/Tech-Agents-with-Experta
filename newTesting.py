import time
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade.template import Template

class Main_Agents(Agent):
        class behavior(FSMBehaviour):
                async def on_start(self):
                        print("behavior started")
                async def on_end(self):
                        print("behavior ended")
        class sending(State):
                async def run(self):
                        msg = Message(to="myagent@jix.im")
                        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                        msg.body = "this is the main agent"
                        await self.send(msg)
                        print("message sent")
                        self.set_next_state("waiting")
        class waiting(State):
                async def run(self):
                        msg = await self.receive(timeout=10)
                        if msg:
                                self.recieved = msg
                                print(f'received the following message: {msg.body}')
                        else:
                                print("no message received after 10 seconds")
                        self.set_next_state("sending")
                
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
                        print("behavior started")
                async def on_end(self):
                        print("behavior ended")
        class sending(State):
                async def run(self):
                        msg = Message(to="someagent@jix.im")
                        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                        msg.body = f'the received message was: {self.received}'
                        await self.send(msg)
                        print("message sent")
                        self.set_next_state("waiting")
        class waiting(State):
                async def run(self):
                        msg = await self.receive(timeout=10)
                        if msg:
                                self.recieved = msg
                                print(f'received the following message: {msg.body}')
                        else:
                                print("no message received after 10 seconds")
                        self.set_next_state("sending")
                
        async def setup(self):
                fsm = self.behavior()
                fsm.add_state(name="sending", state = self.sending())
                fsm.add_state(name="waiting", state = self.waiting(), initial = True)

                fsm.add_transition(source = "sending", dest = "waiting")
                fsm.add_transition(source = "waiting", dest = "sending")
                
                self.add_behaviour(fsm)

main_agent = Main_Agents("someagent@jix.im", "techagent")
auxilary_agent = Auxilary_Agents("myagent@jix.im", "techagent")
auxilary_agent.start()
main_agent.start()

while main_agent.is_alive():
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            auxilary_agent.stop()
            main_agent.stop()
            break
