#!/usr/bin/env python

from setuptools import setup
import os
import os.path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='uwsgi_cli',
    version='1.1',
    description='a simple uwsgi client',
    long_description=open('README.md').read(),
    keywords=["uwsgi", "fengyun", "ruifengyun"],
    url='http://xiaorui.cc',
    author='ruifengyun',
    author_email='rfyiamcool@163.com',
    install_requires=['uwsgi_cli'],
    packages=['uwsgi_cli'],
    license="MIT",
    entry_points={
        'console_scripts': [
            'uwsgi_cli = uwsgi_cli.client:cli',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
