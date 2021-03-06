import logging
import sys
import unittest

from os.path import dirname
from xmlrunner import XMLTestRunner

from boomer.configuration import ConfigurationManager, DEFAULT_CONFIG
from boomer.util.log import setLogLevel

__author__ = 'seanfitz, jdorleans'
if __name__ == "__main__":
    fail_on_error = "--fail-on-error" in sys.argv
    ConfigurationManager.get([DEFAULT_CONFIG, 'boomer.ini'])
    setLogLevel(logging.ERROR)
    tests = unittest.TestLoader().discover(dirname(__file__), "*.py")
    runner = XMLTestRunner("./build/report/tests")
    result = runner.run(tests)

    if fail_on_error and len(result.failures + result.errors) > 0:
        sys.exit(1)
