import codecs
import os.path

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = '0.0.1'

def read(*parts):
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


setup(
    name='uniorm',
    version=VERSION,
    author="Michal Murawski",
    author_email="mmurawski777@gmail.com",
    description="Universal ORM for multiple database backends.",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/micmurawski/dataops/",
    packages=find_packages(exclude=(
        'build',
        'tests',
    )),
    install_requires=[
        "jsonschema==3.2.0",
        "psycopg2-binary==2.9.1"
    ],
    include_package_data=True,
    python_requires='>=3.6',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
)
