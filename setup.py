import os
import setuptools

BASE_URL = "https://github.com/The-LukeZ/"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='TimestringPy',
    version='1.1.3',
    description='Parse a timestring into a floating number.',
    long_description=long_description,
    author='The-LukeZ',
    author_email='luke.hent3005@gmail.com',
    url=BASE_URL + "TimestringPy/",
    packages=setuptools.find_packages(),
    license='MIT',
    long_description_content_type="text/markdown",
    credits=["mike182uk"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
