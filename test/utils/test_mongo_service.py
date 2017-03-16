import unittest
import mock
from mongoengine import Document, StringField, ValidationError
from utils.mongo_service import MongoDBService

class Task(Document):
    name = StringField(required=True, max_length=30)

class MongoServiceTest(unittest.TestCase):

    def setUp(self):
        self.taskService = MongoDBService(Task)

    def test_insert(self):
        "insert should assign the document attributes and save"
        mock_task = mock.MagicMock()
        self.taskService = MongoDBService(mock_task)
        self.taskService.insert({'name': 'Hello'})

        self.assertEqual(mock_task.return_value.name, 'Hello')
        self.assertTrue(mock_task.return_value.save.called)

    def test_insert_without_required_field(self):
        "insert should fail because a field is missing"
        self.taskService = MongoDBService(Task)
        with self.assertRaises(ValidationError) as context:
            self.taskService.insert({})

        self.assertTrue('Field is required' in str(context.exception))

    