
RULES = {
    "Hello": "What's up"
}

class InteractionRedirector:

    def __init__(self):

        self.sessions = {}

    def onInput(self, user_id, message):
        if (user_id in self.sessions.keys()):
            return self.handleSessionInput(self.sessions[user_id], message)
        else:
            return self.handleIdleInput(message)

    def handleIdleInput(self, message):

        if (message in RULES.keys()):
            return RULES[message]
        
    def handleSesssionInput(self, session, message):
        return "Done"