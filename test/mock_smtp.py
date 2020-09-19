"""
Module containing a mock SMTP server for testing email functionality
"""
import asyncore
import re
import smtpd
import threading
from typing import Tuple, List


class MockSMTPServer(smtpd.SMTPServer, threading.Thread):
    """
    A mock SMTP server. Runs in a separate thread so can be started from
    existing test code.
    """

    def __init__(self, hostname: str, port: int):
        threading.Thread.__init__(self)
        smtpd.SMTPServer.__init__(self, (hostname, port), None)
        self.daemon = True
        self.received_messages = []
        self.recipients = []
        self.senders = []
        self.start()

    def run(self):
        """Overridden method that runs the server thread"""
        asyncore.loop()

    def process_message(self, peer: Tuple[str, int], mailfrom: str, rcpttos: List[str], data: bytes, **kwargs):
        """Overridden method that updates the inbox"""
        self.received_messages.append(data.decode('utf-8', errors='replace'))
        self.recipients = self.recipients + rcpttos
        self.senders.append(mailfrom)

    def reset(self):
        """Resets the 'inbox'"""
        self.received_messages = []
        self.recipients = []
        self.senders = []

    def received_message_from(self, sender_email: str):
        """Returns True if the list of senders has the sender_email"""
        return any([email == sender_email for email in self.senders])

    def has_message_for(self, recipient_email: str):
        """Returns True if the list of recipients has the recipient_email"""
        return any([email == recipient_email for email in self.recipients])

    def received_message_matching(self, template: str):
        """Returns true if the list of messages contains a message matching the given template"""
        return any([re.search(template, message) for message in self.received_messages])

    def received_messages_count(self):
        """Returns the number of received messages"""
        return len(self.received_messages)

    def __del__(self):
        """Attempt to close the server before object is deleted"""
        try:
            self.close()
        except Exception:
            pass
