import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

BASE_URL = "https://github.com/The-LukeZ/"

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='TimestringPy',
    version='1.0',
    description='Parse a timestring into a timedelta object.',
    long_description=README,
    author='The-LukeZ',
    author_email='luke.hent3005@gmail.com',
    url=BASE_URL + "TimestringPy/",
    py_modules=['timestring'],
    scripts=['timestring.py'],
    license='MIT',
    long_description_content_type="text/x-md"
)