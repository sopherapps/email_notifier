"""Module with utility functions for exception handling"""
import logging
import traceback
from socket import gethostname

from pydantic import BaseModel

from .general_notifier import GeneralNotifier


class ExceptionNotifier(BaseModel):
    is_exception_in_subject: bool = True
    salutation: str = 'Hi,'
    subject: str = ''

    class Config:
        arbitrary_types_allowed = True

    def notify(self, exception: Exception):
        """Sends a notification of the given exception"""
        exception_name = exception.__class__.__name__
        exception_traceback = traceback.format_exc()
        extended_subject = f'{self.subject}'

        if self.is_exception_in_subject:
            extended_subject = f'{extended_subject} {exception_name}'

        extended_subject = f'{extended_subject} on Host {gethostname()}'

        extended_body = f'''\
        {self.salutation}
        <br /><br />
        <strong>{exception_name}</strong>
        <br />
        <div style="background-color: #ebeff5; padding: 1rem; margin: 1rem;">
            <div style="white-space: pre-line;">
                {exception_traceback}
            </div>
        </div>
        '''

        logging.error(f'{exception_name}\n{exception_traceback}')
        GeneralNotifier.send(subject=extended_subject, body=extended_body, priority=1)
