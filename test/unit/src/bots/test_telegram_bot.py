import unittest
import mock
from src.bots.bot_telegram import start, task, tasks

class TelegramBotTest(unittest.TestCase):

    @mock.patch('usquam.src.bots.bot_telegram.InteractionRedirector')
    def test_start(self, mock_IR):
        mock = mock.MagicMock()
        mock.message.from_user.id = '1'
        mock_IR.onInput.return_value = 'hello'
        start(None, mock)

        self.assertTrue(mock_IR.onInput.called)
        mock.message.reply_text.assert_called_with('hello')