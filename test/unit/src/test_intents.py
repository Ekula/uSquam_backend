import unittest
from src.intent import IntentParser

class TestIntentParser(unittest.TestCase):

    def setUp(self):
        self.IP = IntentParser()

    def test_greetings(self):
        positive = [
            self.IP.parse("hi"),
            self.IP.parse("hello sir"),
            self.IP.parse("good morning")
        ]

        for result in positive:
            self.assertEqual(result['intent_type'], "Greetings")

    def test_expect_different(self):
        result = self.IP.parse("hi", ["NewTask"])
        self.assertEqual(result, None)
        result = self.IP.parse("I would like a task", ["NewTask"])
        self.assertEqual(result['intent_type'], "NewTask")

    def test_task(self):
        positive = [
            self.IP.parse("Can I have another task"),
            self.IP.parse("new task"),
            self.IP.parse("give me a task")
        ]

        for result in positive:
            self.assertEqual(result['intent_type'], "NewTask")

    def test_answer(self):
        result = self.IP.parse("something else")
        self.assertEqual(result['intent_type'], "Answer")
