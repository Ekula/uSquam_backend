import unittest
import mock
from usquam.src.session_interaction_handler import SessionInteractionHandler

class TestSessionInteraction(unittest.TestCase):

    def setUp(self):
        SessionInteractionHandler.handlers = {'Answer': mock.MagicMock(return_value="foo"), 
                                              'CancelTask': mock.MagicMock(return_value="bar")}

    @mock.patch('usquam.src.session_interaction_handler.IntentParser')
    def test_handleInput(self, mock_intent):
        mock_intent.parse.return_value = {'intent_type': 'Answer'}
        result = SessionInteractionHandler.handleInput(None, "hello")
        
        mock_intent.parse.assert_called_with("hello", ["Answer", "CancelTask"])
        self.assertEquals(result, 'foo')
        SessionInteractionHandler.handlers['Answer'].assert_called_with(None, "hello")