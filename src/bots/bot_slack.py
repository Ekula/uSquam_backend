from slackclient import SlackClient
from utils.secrets import SLACKBOT_KEY
from src.interaction_redirector import InteractionRedirector
import time
import logging
import threading

class SlackBot(threading.Thread):

    def __init__(self):
        self.event = threading.Event()
        threading.Thread.__init__(self, args=(self.event,))
        self.sc = SlackClient(SLACKBOT_KEY)

    def handleMessage(self, user_id, message):
        result = InteractionRedirector.onInput(user_id, message)
        return result
        
    def handleStream(self, stream):
        
        for event in stream:
            if event['type'] == 'message' and not 'subtype' in event:
                try:
                    answer = self.handleMessage(event['user'], event['text'])
                    self.sc.api_call(
                        "chat.postMessage",
                        channel=event['channel'],
                        text=answer
                    )
                except:
                    logging.warning(event)


    def run(self):
        logging.debug("SlackBot started")

        if not self.sc.rtm_connect():
            logging.warning("Could not connect to Slack Realt-time messaging")

        while not self.event.isSet():
            stream = self.sc.rtm_read()
            self.handleStream(stream)
            time.sleep(1)

        logging.debug("SlackBot has stopped")

    def stop(self):
        self.event.set()

# sc = SlackClient(SLACKBOT_KEY)

# if sc.rtm_connect():
#     while True:
#         print sc.rtm_read()
#         time.sleep(1)
# else:
#     print "Connection failed"


