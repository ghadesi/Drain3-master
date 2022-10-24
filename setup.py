# SPDX-License-Identifier: MIT

from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Drain3-amin',
    packages=['drain3'],
    version="0.0.1",
    license='MIT',
    description="Persistent & streaming log template miner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Amin Ghadesi(Fork IBM Research Haifa)",
    author_email="amin.ghadesi@gmail.com",
    url="https://github.com/ghadesi/Drain3-master",
    download_url='https://github.com/ghadesi/Drain3-master/dist/v_01.tar.gz',
    keywords=['drain', 'log', 'parser', 'ghadesi', 'template', 'logs', 'miner'],
    install_requires=['jsonpickle==1.5.1', 'cachetools==4.2.1'],
    extras_require={
        "kafka": ['kafka-python==2.0.1'],
        "redis": ['redis==3.5.3'],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
