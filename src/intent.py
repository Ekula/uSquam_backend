import json
import sys
import os
import fnmatch
import logging
from adapt.intent import IntentBuilder
from adapt.engine import DomainIntentDeterminationEngine



# engine.register_domain('Domain1')
# engine.register_domain('Domain2')

class IntentParser:

    def __init__(self):

        self.engine = DomainIntentDeterminationEngine()

        # Load all files in ./intents
        matches = []
        for root, dirnames, filenames in os.walk(os.path.join(os.path.dirname(__file__),'intents')):
            for filename in fnmatch.filter(filenames, '*.json'):
                path = os.path.join(root, filename)
                matches.append(path)

        if len(matches) == 0:
            raise Exception("No intent specifications found at ", os.path.join(os.path.dirname(__file__),'intents'))

        for path in matches:
            with open(path) as file:
                if not self.loadIntentSpec(root.split('/')[-1], json.load(file)):
                    logging.warning("Something went wrong during parsing of ", os.path.join(os.path.dirname(__file__),'intents'))
                
        
    def loadIntentSpec(self, domain, data):

        if not 'intent' in data:
            return False

        if not domain in self.engine.domains:
            self.engine.register_domain(domain)
        
        new_intent = IntentBuilder(data['intent'])

        if 'required' in data:
            for entity in data['required']:
                for key, value in entity.iteritems():
                    for keyword in value:
                        self.engine.register_entity(keyword, key, domain=domain)

                new_intent = new_intent.require(key)
        
        if 'optionally' in data:
            for entity in data['optionally']:
                for key, value in entity.iteritems():
                    for keyword in value:
                        self.engine.register_entity(keyword, key, domain=domain)
                
                new_intent = new_intent.optionally(key)

        new_intent = new_intent.build()
        self.engine.register_intent_parser(new_intent, domain=domain)
        
        return True

    def parse(self, text):
        """
        Returns best match for intent.
        """

        for intent in self.engine.determine_intent(text):
            if intent and intent.get('confidence') > 0.0:
                return intent



if __name__ == "__main__":
    IP = IntentParser()
    print IP.parse("Hello")
    print IP.parse("Done")