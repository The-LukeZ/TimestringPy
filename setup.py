import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

BASE_URL = "https://github.com/The-LukeZ/"

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='TimestringPy',
    version='1.1.2',
    description='Parse a timestring into a floating number.',
    long_description='file:README.md',
    author='The-LukeZ',
    author_email='luke.hent3005@gmail.com',
    url=BASE_URL + "TimestringPy/",
    packages=find_packages(),
    license='MIT',
    long_description_content_type="text/markdown",
    credits=["mike182uk"]
)