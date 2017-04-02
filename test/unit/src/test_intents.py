import unittest
from src.intent import IntentParser

class TestIntentParser(unittest.TestCase):

    def test_greetings(self):
        positive = [
            IntentParser.parse("hi"),
            IntentParser.parse("hello sir"),
            IntentParser.parse("good morning")
        ]

        for result in positive:
            self.assertEqual(result['intent_type'], "Greetings")

    def test_expect_different(self):
        result = IntentParser.parse("hi", ["NewTask"])
        self.assertEqual(result, None)
        result = IntentParser.parse("I would like a task", ["NewTask"])
        self.assertEqual(result['intent_type'], "NewTask")

    def test_task(self):
        positive = [
            IntentParser.parse("Can I have another task"),
            IntentParser.parse("new task"),
            IntentParser.parse("give me a task")
        ]

        for result in positive:
            self.assertEqual(result['intent_type'], "NewTask")

    def test_answer(self):
        result = IntentParser.parse("something else")
        self.assertEqual(result['intent_type'], "Answer")
