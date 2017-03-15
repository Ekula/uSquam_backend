import unittest
import mock
from usquam.resources.task.service import Service
from mongoengine import ValidationError, DoesNotExist

class TaskServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = Service()

    @mock.patch("usquam.resources.task.service.Task")
    def test_insert(self, mock_task):
        "insert should call the save method"
        self.service.insert({"name": "Hello"})

        self.assertEqual(mock_task.return_value.name, "Hello")
        self.assertTrue(mock_task.return_value.save.called)

    def test_insert_name_too_long(self):
        "insert should fail because the name is too long"
        name = "Hellodhsfkjahsdfljhaslkdjfhlkashdfasdhflkjahsl"
        with self.assertRaises(ValidationError) as context:
            self.service.insert({"name": name})

        self.assertTrue('String value is too long' in str(context.exception))

    @mock.patch("usquam.resources.task.service.Task")
    def test_get(self, mock_task):
        "get should return the retrieved item"
        mock_task.objects.get.return_value = {'name': 'Hello'}
        item = self.service.get("1")

        self.assertEqual(item, {"name":"Hello"})

    def test_get_wrong_id(self):
        "get should fail on wrong id"
        with self.assertRaises(DoesNotExist) as context:
            self.service.get("4f4381f4e779897a2c000009")

    @mock.patch("usquam.resources.task.service.Task")
    def test_getAll(self, mock_task):
        "get should return the retrieved item"
        mock_task.objects = [{'name': 'Hello'}, {'name': 'World'}]
        items = self.service.getAll()

        self.assertEqual(items, [{'name': 'Hello'}, {'name': 'World'}])