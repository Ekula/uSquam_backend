import unittest
import mock
from usquam.src.bots.bot_telegram import start, task, tasks

class TelegramBotTest(unittest.TestCase):

    @mock.patch('usquam.src.bots.bot_telegram.InteractionRedirector')
    def test_start(self, mock_IR):
        mock_update = mock.MagicMock()
        mock_update.message.from_user.id = '1'
        mock_IR.onInput.return_value = 'hello'
        start(None, mock_update)

        self.assertTrue(mock_IR.onInput.called)
        mock_update.message.reply_text.assert_called_with('hello')