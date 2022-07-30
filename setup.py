from setuptools import setup
setup(
    name='pycom',
    version='1.0.0',
    entry_points={
        'console_scripts': [
            'pycom=pycom.pycom:main'
        ]
    }
)