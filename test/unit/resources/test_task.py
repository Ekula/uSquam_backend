import unittest
import mock
import json
import usquam
from flask import request
from usquam.app import app

class TaskTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        pass

    @mock.patch("usquam.resources.task.blueprint.TaskService")
    def test_get(self, mock_service):
        "GET /tasks/:id should return 200 and a task"
        mock_service.get.return_value = {"id": 1}

        result = self.app.get('/tasks/0')
        body = json.loads(result.data)

        self.assertDictEqual(body, {"id": 1})

    @mock.patch("usquam.resources.task.blueprint.TaskService")
    def test_get_empty(self, mock_service):
        "GET /tasks/:id should return 404 when no tasks are there"
        mock_service.get.return_value = None

        result = self.app.get('/tasks/0')
        body = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(body, None)

    @mock.patch("usquam.resources.task.blueprint.TaskService")
    def test_post(self, mock_service):
        "POST /tasks should call the insert method of the service with data and return 200"
        result = self.app.post('/tasks', 
            data=json.dumps(dict({'id': 2})),
            content_type='application/json')
        
        mock_service.insert.assert_called_with({'id': 2})
        self.assertEqual(result.status_code, 200)

    @mock.patch("usquam.resources.task.blueprint.TaskService")
    def test_post_empty(self, mock_service):
        "POST /tasks should call the insert method of the service without data and return 404"
        mock_service.insert.return_value = False
        result = self.app.post('/tasks')
        
        self.assertTrue(mock_service.insert.called)
        mock_service.insert.assert_called_with(None)
        self.assertEqual(result.status_code, 404)