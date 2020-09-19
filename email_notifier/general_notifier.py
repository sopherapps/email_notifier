"""
Utility Functions for sending email
"""
import logging
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List


class GeneralNotifier:
    host: str = os.getenv('MAIL_SERVER_HOST', 'smtp.office365.com')
    port: int = int(os.getenv('MAIL_SERVER_PORT', '587'))
    username: str = os.getenv('DEFAULT_SENDER_EMAIL_ADDRESS', '')
    password: str = os.getenv('DEFAULT_SENDER_EMAIL_PASSWORD', '')
    subject_prefix: str = os.getenv('DEFAULT_EMAIL_SUBJECT_PREFIX', '')
    email_signature: str = os.getenv('DEFAULT_EMAIL_SIGNATURE', '')
    default_recipients: List[str] = [
        email.strip() for email in os.getenv('DEFAULT_EMAIL_RECIPIENTS', '').split(',')
    ]

    @classmethod
    def _start_tls(cls, server: smtplib.SMTP):
        """Starts an SSL connection attempt"""
        try:
            context = ssl.create_default_context()
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        except smtplib.SMTPNotSupportedError as exp:
            logging.info('Email SMTP server does not support SSL')

    @classmethod
    def _login(cls) -> Optional[smtplib.SMTP]:
        """Logs into the SMTP server and returns the server"""
        server = smtplib.SMTP(cls.host, cls.port)
        cls._start_tls(server=server)

        try:
            server.login(cls.username, cls.password)
        except smtplib.SMTPNotSupportedError as exp:
            logging.info('Email SMTP server does not support authentication')

        return server

    @classmethod
    def _construct_message(cls, subject: str, body: str, recipients: List[str], priority: int = 3) -> str:
        """Constructs a message to be sent via email"""
        message = MIMEMultipart("alternative")
        message["Subject"] = f"{cls.subject_prefix}{subject}"
        message["From"] = cls.username
        message["To"] = ','.join(recipients)
        message['X-Priority'] = f'{priority}'

        if priority == 1:
            message['X-MSMail-Priority'] = 'High'
            message['Importance'] = 'High'

        text = f"""
        {body}

        {cls.email_signature}
        """

        html = f"""
        <html>
            <body>
                <div>{body}</div>
                <br />
                <div>{cls.email_signature}</div>
            </body>
        </html>
        """
        # Turn these into plain/html MIMEText objects
        main_message_part = MIMEText(html, 'html')
        backup_message_part = MIMEText(text, 'text')
        # Attach the MIMEText objects. Email client attempts the last part first
        message.attach(backup_message_part)
        message.attach(main_message_part)

        return message.as_string()

    @classmethod
    def send(cls, subject: str, body: str, recipients: Optional[List[str]] = None, priority: int = 3):
        """Sends the email"""
        server: Optional[smtplib.SMTP] = None
        return_value = None

        try:
            server = cls._login()
            recipient_emails = cls.default_recipients if recipients is None else recipients
            message = cls._construct_message(subject=subject, body=body, recipients=recipient_emails)
            return_value = server.sendmail(from_addr=cls.username, to_addrs=recipient_emails, msg=message)
        except Exception as exp:
            logging.error(exp)
        finally:
            if server is not None:
                server.quit()

        return return_value
