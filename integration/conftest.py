import platform

import pytest
import os

@pytest.fixture
def pycom_path():
	working_dir = os.getcwd()
	return os.path.join(working_dir, 'src', 'pycom', 'pycom.py')


@pytest.fixture
def run_check_compile(pycom_path):
	def check_compile(file: str):
		# Runs a compilation check then returns a status code
		# Successful compilation returns 0
		return os.system(f"{pycom_path} -c {file}")

	return check_compile
