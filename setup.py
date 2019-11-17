# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wsgigo',
    version='1.2.0',
    description='Simple wsgi app that routes requests to other wsgi apps. A WSGI router.',
    long_description=long_description,
    url='https://github.com/kkinder/wsgigo',
    author='Ken Kinder',
    author_email='ken@kkinder.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='wsgi router routing',
    packages=find_packages(exclude=['examples', 'tests'])
)
