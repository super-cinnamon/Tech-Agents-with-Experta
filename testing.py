import json
import pprint


pp = pprint.PrettyPrinter(indent=4)

file = open("magasin1.json")

data = json.load(file)


#pp.pprint(data)
#pp.pprint(data["2"])


######################################################################################################################
################################################# AGENTS ############################################################

import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template


class SenderAgent(Agent):
    def setmsg(self, message):
            self.message = message
    
    class InformBehav(OneShotBehaviour):
        def set_message(self, message):
            self.message = message
        
        async def run(self):
            print("InformBehav running")
            msg = Message(to="myagent@jix.im")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = self.message                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        b.set_message(self.message)
        self.add_behaviour(b)

class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")
            
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            #await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_mtadata("performative", "inform")
        self.add_behaviour(b, template)

class MainAgent(Agent):
    def setmsg(self, message):
            self.message = message
    class sendBehav(CyclicBehaviour):
        def set_message(self, message):
            self.message = message

        async def run(self):
            #sending
            msg = Message(to="myagent@jix.im")
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = self.message
            await self.send(msg)
            print("message sent")
            
    class RecBehave(CyclicBehaviour):
        async def run(self):
            await self.agent.send.join()
            reply = await self.receive(timeout=30)
            if reply:
                print("message received: {}".format(reply.body))
            else: 
                print("no message received after 30 seconds")
            await self.agent.stop()

    
    async def setup(self):
        self.send = self.sendBehav()
        self.send.set_message(self.message)
        self.add_behaviour(self.send)
        self.receive = self.RecBehave()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.receive, template)

class AuxilaryAgent(Agent):
    def setmsg(self, message):
            self.message = message
    class sendBehav(CyclicBehaviour):
        def set_message(self, message):
            self.message = message

        async def run(self):
            #sending
            await self.agent.receive.join()
            msg = Message(to="someagent@jix.im")
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = f'hi this is aux i receieved : {msg}'
            await self.send(msg)
            await self.agent.stop()
            
    class RecBehave(CyclicBehaviour):
        async def run(self):
            reply = await self.receive(timeout=30)
            if reply:
                print("message received: {}".format(reply.body))
            else: 
                print("no message received after 30 seconds")
    async def setup(self):
        self.receive = self.RecBehave()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.receive, template)
        self.send = self.sendBehav()
        #send.set_message(self.message)
        self.add_behaviour(self.send)


if __name__ == "__main__":
    #receiveragent = ReceiverAgent("firstagent@jix.im", "techagent")
    # receiveragent = ReceiverAgent("myagent@jix.im", "techagent")
    # future = receiveragent.start()
    # future.result() # wait for receiver agent to be prepared.
    # #senderagent = SenderAgent("mainagent@jix.im", "techagent")

    # senderagent = SenderAgent("secondagent@jix.im", "techagent")
    # senderagent2 = SenderAgent("someagent@jix.im", "techagent")
    # senderagent.setmsg("agent1")
    # senderagent2.setmsg("agent2")
    # senderagent.start()
    # future.result()
    # senderagent2.start()

    # while receiveragent.is_alive():
    #     try:
    #         time.sleep(5)
    #     except KeyboardInterrupt:
    #         senderagent.stop()
    #         senderagent2.stop()
    #         receiveragent.stop()
    #         break


    main_agent = MainAgent("someagent@jix.im", "techagent")
    auxilary_agent = AuxilaryAgent("myagent@jix.im", "techagent")
    future = auxilary_agent.start()
    future.result()
    main_agent.setmsg("hello, this is main agent")
    
    future2 = main_agent.start()
    future2.result()
    main_agent.receive.join()
    auxilary_agent.send.join()
    

    while main_agent.is_alive():
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            auxilary_agent.stop()
            main_agent.stop()
            break

    print("Agents finished")

