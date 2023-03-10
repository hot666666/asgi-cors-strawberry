from setuptools import setup, find_packages
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="asgi-cors-strawberry",
    description="ASGI middleware for CORS, especially for using strawberry[channels]",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Hot666666",
    url="https://github.com/hot666666/asgi-cors-strawberry",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=find_packages(),
)