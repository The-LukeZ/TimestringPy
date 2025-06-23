import setuptools

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except:
    long_description = "Parse a timestring into a floating number."

setuptools.setup(
    name='TimestringPy',
    version='1.2.0',
    description='Parse a timestring into a floating number.',
    long_description=long_description,
    author='The-LukeZ',
    maintainer='The-LukeZ',
    url="https://github.com/The-LukeZ/TimestringPy",
    packages=setuptools.find_packages(),
    license='MIT',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
