import json
import pprint


pp = pprint.PrettyPrinter(indent=4)

file = open("magasin1.json")

data = json.load(file)


pp.pprint(data)
pp.pprint(data["2"])


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
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)



if __name__ == "__main__":
    #receiveragent = ReceiverAgent("firstagent@jix.im", "techagent")
    receiveragent = ReceiverAgent("myagent@jix.im", "techagent")
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.
    #senderagent = SenderAgent("mainagent@jix.im", "techagent")

    senderagent = SenderAgent("secondagent@jix.im", "techagent")
    senderagent2 = SenderAgent("someagent@jix.im", "techagent")
    senderagent.setmsg("agent1")
    senderagent2.setmsg("agent2")
    senderagent.start()
    future.result()
    senderagent2.start()

    while receiveragent.is_alive():
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            senderagent.stop()
            senderagent2.stop()
            receiveragent.stop()
            break
    print("Agents finished")

