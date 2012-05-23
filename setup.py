#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='fspyrpc',
    version='0.0.1',
    description='A simple RPC-framework written in Python',
    long_description=open('README.md').read(),
    author='Florian Schlachter',
    author_email='flori@n-schlachter.de',
    url='https://bitbucket.org/flosch/pyrpc',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    zip_safe=False,
    #test_suite='tests',
    install_requires=open("requirements.txt", "r").read().split()
)