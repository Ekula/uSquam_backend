import unittest
import mock
from usquam.resources.task.service import Service

class TaskServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = Service()

    @mock.patch("usquam.resources.task.service.Task")
    def test_insert(self, mock_task):
        "insert should call the save method"
        self.service.insert({"name": "Hello"})

        self.assertEqual(mock_task.return_value.name, "Hello")
        self.assertTrue(mock_task.return_value.save.called)