import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="email_notifier",
    version="0.0.1",
    description="A simple email notifier for general messages or exceptions with easy environment configuration",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sopherapps/email_notifier",
    author="Martin Ahindura",
    author_email="team.sopherapps@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=["pydantic"],
    entry_points={
    },
)