import coverage
import unittest
import os
from io import StringIO
import sys
from contextlib import redirect_stdout

def has_test_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(pattern):
                return True
    return False

# Run coverage on file and return coverage percentage.
def run_coverage_for_file(file_path):
    file_dir = os.path.dirname(file_path)
    if not file_dir:
        file_dir = '.'
    test_pattern = '_test.py'
    if not has_test_files(file_dir, test_pattern):
        return 0, 0  # Return 0% coverage and 0 defect density if no test files are found

    cov = coverage.Coverage(source=['main'])
    cov.start()

    # Run tests in files ending in _test.py, send stdout to /dev/null (prevents printing in console)
    with open(os.devnull, 'w') as fnull:
        with redirect_stdout(fnull):
            loader = unittest.TestLoader()
            suite = loader.discover(file_dir, pattern='*_test.py')
            runner = unittest.TextTestRunner(stream=fnull, verbosity=0)
            result = runner.run(suite)

    cov.stop()
    cov.save()

    # Get total # of tests
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    defect_density = failed_tests / total_tests

    if not cov.get_data().measured_files():
        print("No data was collected.")
        coverage_percent = 0.0
    else:
        # Generate the HTML coverage report
        html_cov_folder = os.path.join(get_root_directory(), 'htmlcov')
        cov.html_report(directory=html_cov_folder)

        # Generate the coverage report and obtain data
        covered = cov.analysis(file_path)[1]
        missed = cov.analysis(file_path)[2]
        coverage_percent = 100 * len(covered) / (len(covered) + len(missed))

    return coverage_percent, defect_density

# Get root directory
def get_root_directory():
    return os.path.dirname(os.path.abspath(__file__))