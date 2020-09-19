# email_notifier

A simple email notifier for general messages or exceptions with easy environment configuration

## Description

`email_notifier` comprises two notifier classes that send emails to a given set of recipients

### GeneralNotifier

Sends a general message to a number of recipient emails.

### ExceptionNotifier

Sends a nicely formatted exception alert with an appropriate stack trace to a number of recipient emails.

## Main Dependencies

- [Python +3.6](https://www.python.org)
- [pydantic](https://github.com/samuelcolvin/pydantic/)

## Getting Started

- Install the package

  ```bash
  pip install email_notifier
  ```

- Set the environment variables in case you wish wish to have default settings for your email notifier

- Import the `GeneralNotifier` and the `ExceptionNotifier` classes and use accordingly

  ```python
  from email_notifier import GeneralNotifier, ExceptionNotifier

  # Assuming the environment variables have been set
  # MAIL_SERVER_HOST=127.0.0.1
  # MAIL_SERVER_PORT=10025
  # DEFAULT_SENDER_EMAIL_ADDRESS=anne@example.com
  # DEFAULT_SENDER_EMAIL_PASSWORD=password123123
  # DEFAULT_EMAIL_SUBJECT_PREFIX="Test: "
  # DEFAULT_EMAIL_SIGNATURE="Regards<br/>Sender"
  # DEFAULT_EMAIL_RECIPIENTS=paul@example.com, albert@example.com

  general_notifier = GeneralNotifier()
  general_notifier.send(subject="....", body="....", recipients=["..@...com", "...@...com")

  # if recipients are not provided, the notifier sends to the default email recipients
  general_notifier.send(subject="....", body="....")

  exception_notifier = ExceptionNotifier(is_exception_in_subject=True, subject="...", salutation="...")
  # The defaults also work in this case
  # exception_notifier = ExceptionNotifier()

  def func():
      """Just a trial function with exception handling"""
      try:
          raise IndexError("Just raising a random exception for exhibition purposes")
      except IndexError as exp:
          # an email is sent and the python logger logs the exception
          exception_notifier.notify(exp)

  # When the function is called, the notifier will do the needful
  func()
  ```

## How to test

- Clone the repo and enter its root folder

  ```bash
  git clone https://github.com/sopherapps/email_notifier.git && cd email_notifier
  ```

- Copy the `.example.env` file to `.env` and make appropriate edits on it

  ```bash
  cp .example.env .env
  ```

- Create a virtual environment and activate it

  ```bash
  virtualenv -p /usr/bin/python3.6 env && source env/bin/activate
  ```

- Install the dependencies

  ```bash
  pip install -r requirements.txt
  ```

- Run the test command

  ```bash
  python -m unittest
  ```

## Environment Configuration

The package leverages environment settings in say a `.env` file or set directly.
The environment variables include the following.

| Environment Variable          | What it is for                            | Default            |
| ----------------------------- | ----------------------------------------- | ------------------ |
| MAIL_SERVER_HOST              | The SMTP host                             | smtp.office365.com |
| MAIL_SERVER_PORT              | The SMTP port                             | 587                |
| DEFAULT_SENDER_EMAIL_ADDRESS  | sender email address                      | ""                 |
| DEFAULT_SENDER_EMAIL_PASSWORD | sender email password                     | ""                 |
| DEFAULT_EMAIL_SUBJECT_PREFIX  | subject prefix                            | ""                 |
| DEFAULT_EMAIL_SIGNATURE       | email signature                           | ""                 |
| DEFAULT_EMAIL_RECIPIENTS      | comma separated recipient email addresses | ""                 |

## Acknowledgements

This [Real Python tutorial on sending emails with python](https://realpython.com/python-send-email) was very helpful.
This [Real Python tutorial on publishing packages](https://realpython.com/pypi-publish-python-package/) was very helpful

## License

Copyright (c) 2020 [Martin Ahindura](https://github.com/Tinitto) Licensed under the [MIT License](./LICENSE)
