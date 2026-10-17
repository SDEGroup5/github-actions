"""
This file contain the script that execute the various tests and see if they all pass
"""

import json
import os
import subprocess
import sys

CODE_COVERAGE_THRESHOLD: int = 80
COVERAGE_FILE_NAME: str = ".coverage.json"


def execute_test() -> int:
    '''
    Let pytest execute all tests: if they all pass, 0 will be returned, otherwise 1.
    Note that pytest return 0 if all test pass, 1 otherwise.
    A file for the code coverage will also be created with name: .coverage.json
    '''

    if os.path.exists(COVERAGE_FILE_NAME):
        os.remove(COVERAGE_FILE_NAME)

    try:
        result: int = subprocess.call([
            'pytest', "--cov=backend",
            f"--cov-report=json:{COVERAGE_FILE_NAME}"
        ],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL,
                                      shell=False)
    except (OSError, subprocess.SubprocessError) as err:
        if os.path.exists(COVERAGE_FILE_NAME):
            os.remove(COVERAGE_FILE_NAME)
        print("An exception was raised during test: ", err)
        return 1

    if result:
        os.remove(COVERAGE_FILE_NAME)
        print("Test executed: at least one test did not pass")
    else:
        print("Test executed: all passed")

    return result


def read_coverage_result() -> int:
    '''
    Check whether the code coverage is over a definable threshold.
    Return 0 if threshold is satisfied, 1 otherwise
    '''

    try:
        with open(COVERAGE_FILE_NAME, encoding="utf-8") as f:
            coverage = json.load(f)
    except (OSError, json.JSONDecodeError) as err:
        print(f"An exception was raised during coverage check: {err}.",
              "This is probably normal if at least one test failed.")
        return 1

    total = int(coverage["totals"]["percent_statements_covered_display"])

    result = total >= CODE_COVERAGE_THRESHOLD

    if result:
        print(
            f"Coverage does satisfy threshold: {total}% over {CODE_COVERAGE_THRESHOLD}%"
        )
    else:
        print(
            f"Coverage does NOT satisfy threshold: {total}% over {CODE_COVERAGE_THRESHOLD}%"
        )

    return not result


def main():
    '''
    Main script
    '''

    test_result = execute_test()
    test_coverage_result = read_coverage_result()

    sys.exit(test_result or test_coverage_result)


if __name__ == "__main__":
    main()
