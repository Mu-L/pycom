from setuptools import setup

setup(
    name='pycom',
    version='1.1.0',
    entry_points={
        'console_scripts': [
            'pycom=pycom.main:main'
        ]
    }
)
