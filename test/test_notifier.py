"""Tests for the GeneralNotifier class"""
# import logging
import logging
import os
from socket import gethostname
from traceback import format_exc
from unittest import TestCase, main
from unittest.mock import Mock, patch

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from test.mock_smtp import MockSMTPServer
from email_notifier import GeneralNotifier, ExceptionNotifier


class TestNotifier(TestCase):
    """Test class for the GeneralNotifier and the ExceptionNotifier classes"""
    mock_server: MockSMTPServer

    @classmethod
    def setUpClass(cls) -> None:
        cls.mock_server = MockSMTPServer(
            hostname=os.getenv('MAIL_SERVER_HOST', '127.0.0.1'),
            port=int(os.getenv('MAIL_SERVER_PORT', 10025)))

    def setUp(self) -> None:
        """Initialize some variables"""
        self.subject_prefix = os.getenv('DEFAULT_EMAIL_SUBJECT_PREFIX', '')
        self.notifier = GeneralNotifier()
        self.subject = 'Hello World'
        self.salutation = 'Hi there'
        self.body = 'Hi there'
        self.sender = os.getenv('DEFAULT_SENDER_EMAIL_ADDRESS')
        self.recipients = [
            email.strip() for email in os.getenv('NON_DEFAULT_EMAIL_RECIPIENTS', '').split(',')]
        self.default_recipients = [
            email.strip() for email in os.getenv('DEFAULT_EMAIL_RECIPIENTS', '').split(',')]

    def test_general_notifier_send(self):
        """Should send message to a given set of recipients"""
        self.assertEqual(self.mock_server.received_messages_count(), 0)
        self.notifier.send(subject=self.subject, body=self.body, recipients=self.recipients)
        self.assertGreater(self.mock_server.received_messages_count(), 0)

        self.assertTrue(all([self.mock_server.has_message_for(recipient) for recipient in self.recipients]))
        self.assertTrue(self.mock_server.received_message_from(self.sender))
        self.assertTrue(self.mock_server.received_message_matching(self.body))
        self.assertTrue(self.mock_server.received_message_matching(f'Subject: {self.subject_prefix}{self.subject}'))

    def test_general_notifier_send_default_recipients(self):
        """If no recipients are provided, it sends to those in the environment"""
        self.assertEqual(self.mock_server.received_messages_count(), 0)
        self.notifier.send(subject=self.subject, body=self.body)
        self.assertGreater(self.mock_server.received_messages_count(), 0)

        self.assertTrue(all([self.mock_server.has_message_for(recipient) for recipient in self.default_recipients]))
        self.assertTrue(self.mock_server.received_message_from(self.sender))
        self.assertTrue(self.mock_server.received_message_matching(self.body))
        self.assertTrue(self.mock_server.received_message_matching(f'Subject: {self.subject_prefix}{self.subject}'))

    def test_exception_notifier_notify_email(self):
        """Should send email of the exception to the recipients set in the environment"""
        notifier = ExceptionNotifier(subject=self.subject, salutation=self.salutation, is_exception_in_subject=False)

        def trial_function():
            try:
                raise ValueError('Dummy error')
            except ValueError as exp:
                notifier.notify(exp)

        trial_function()

        host = gethostname()
        subject = f'{self.subject_prefix}{self.subject} on Host {host}'
        self.assertEqual(self.mock_server.received_messages_count(), 1)
        self.assertTrue(all([self.mock_server.has_message_for(recipient) for recipient in self.default_recipients]))
        self.assertTrue(self.mock_server.received_message_from(self.sender))
        self.assertTrue(self.mock_server.received_message_matching(self.salutation))
        self.assertTrue(self.mock_server.received_message_matching(f'Subject: {subject}'))
        self.assertTrue(self.mock_server.received_message_matching(r'Traceback \(most recent call last\)'))

    def test_exception_notifier_default_notify_email(self):
        """Should send email of the exception to the recipients set in the environment"""
        notifier = ExceptionNotifier()

        def trial_function():
            try:
                raise ValueError('Dummy error')
            except ValueError as exp:
                notifier.notify(exp)

        trial_function()

        exception_name = 'ValueError'
        host = gethostname()
        subject = f'{self.subject_prefix} {exception_name} on Host {host}'

        self.assertEqual(self.mock_server.received_messages_count(), 1)
        self.assertTrue(all([self.mock_server.has_message_for(recipient) for recipient in self.default_recipients]))
        self.assertTrue(self.mock_server.received_message_from(self.sender))
        self.assertFalse(self.mock_server.received_message_matching(self.salutation))
        self.assertTrue(self.mock_server.received_message_matching(f'Subject: {subject}'))
        self.assertTrue(self.mock_server.received_message_matching(r'Traceback \(most recent call last\)'))

    @patch.object(logging, 'error')
    def test_exception_notifier_notify_log(self, mocked_error_logger: Mock):
        """Should log the exception using the python logger"""
        notifier = ExceptionNotifier()

        def trial_function():
            try:
                raise ValueError('Dummy error')
            except ValueError as exp:
                notifier.notify(exp)
                return format_exc()

        exception_traceback = trial_function()

        exception_name = 'ValueError'
        mocked_error_logger.assert_called_with(f'{exception_name}\n{exception_traceback}')

    def tearDown(self) -> None:
        """Reset the mock SMTP server"""
        self.mock_server.reset()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_server.close()


if __name__ == '__main__':
    main()
