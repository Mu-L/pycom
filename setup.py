import pathlib

import pkg_resources
from setuptools import setup

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='pycom',
    version='1.1.0',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pycom=pycom.main:main'
        ]
    }
)
