#!/usr/bin/python3
import os
import re
import subprocess

import setuptools


def extract_version(filename):
    with open(filename, 'r') as fh:
        for line in fh:
            match = re.match(
                r'''VERSION\s*=\s*["']([-_.0-9a-z]+)(\+?)["']''', line)
            if match:
                if match[2] == '':
                    return match[1]
                else:
                    return match[1] + '.post'
    exit("Cannot extract version number from %s" % filename)


def describe_or_extract_version(filename):
    if 'FORCE_VERSION' in os.environ:
        return os.environ['FORCE_VERSION']
    ret = subprocess.run(['git', 'describe'], capture_output=True, text=True)
    if ret.returncode != 0:
        return extract_version(filename)
    else:
        match = re.match('^v?([0-9]+.[0-9]+.[0-9]+)(-([0-9]+))?', ret.stdout)
        if match:
            if match[3] is None:
                return match[1]
            else:
                return match[1] + '.post' + match[3]
        else:
            return extract_version(filename)


with open('README.md', 'r') as fh:
    long_description = fh.read()
long_description = long_description.replace(
    '<img src="./imgs/', '<img src="https://github.com/MarcelWaldvogel/signale.py/raw/master/imgs/')

setuptools.setup(
    name="signale-logging",
    version=describe_or_extract_version('signale/__init__.py'),
    author="Shardul Nalegave and Marcel Waldvogel",
    author_email="nalegaveshardul40@gmail.com, marcel.waldvogel@trifence.ch",
    description="Elegant Console Logger For Python Command Line Apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcelWaldvogel/signale.py",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['setuptools'],
    python_requires='>=3.2',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "Topic :: System :: Logging",
    ],
)
