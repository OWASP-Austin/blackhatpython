from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList
import random

# This module is good for testing web app services
# that don't allow you to use traditional tools
# e.g.:
# such as a binary protocol wrapped in HTTP traffic.


class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
  def registerExtenderCallbacks(self, callbacks):
    self._callbacks = callbacks
    self._helpers = callbacks.getHelpers()

    callbacks.registerIntruderPayloadGeneratorFactory(self)

    return

  def getGeneratorName(self):
    return "BHP Payload Generator"

  def createNewInstance(self, attack):
    return BHPFuzzer(self, attack)

class BHPFuzzer(IIntruderPayloadGenerator):
    def _init_(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0

        return

def hasMorePayloads(self):
    if self.num_iterations == self.max_payloads:
        return False
    else:
        return True

def getNextPayload(self, current_payload):
    # convert into a string
    payload = "".join(chr(x) for x in current_payload)

    # call our simple mutator to fuzz the POST
    payload = self.mutate_payload(payload)

    # increase the number of fuzzing attempts
    self.num_iteratinos += 1

    return payload

def reset(self):
    self.num_iterations = 0
    return

def mutate_payload(self, original_payload):
    # pick a simple mutator or even call an external script
    picker = random.randint(1,3)

    # select a random offset in the payload to mutate
    offset = random.randint(0, len(original_payload)-1)
    payload = original_payload[:offset]

    # random offset insert a SQL injection attempt
    if picker == 1:
        payload += "'"

    # jam an XSS attempt in
    if picker == 2:
        payload += "<script>alert('BHP!')</script>"

    # repeat a chunk of the original_payload a random number
    if picker == 3:

        chunk_length = random.randint(len(payload[:offset]), len(payload)-1)
        repeater = random.randint(1,10)

        for i in range(repeater):
            payload += original_payload[offset:offset+chunk_length]

    # add the remaining bits of the payload
    payload += original_payload[offset:]

    return payload
