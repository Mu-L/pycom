import pytest
import os


integration_files_path = os.path.join(os.getcwd(), 'integration', 'files')


@pytest.mark.parametrize('filename', [
	'functions.py',
	'list_operations.py',
	'listcomp.py',
	'loops.py',
	'mathlib.py',
	'strings.py'
])
def check_compilation_test(run_check_compile, filename):
	file = os.path.join(integration_files_path, filename)
	return_code = run_check_compile(file=file)
	assert not return_code
