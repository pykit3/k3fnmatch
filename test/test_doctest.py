import doctest
import unittest

import k3fnmatch
import k3fnmatch.pattern


class TestDoctest(unittest.TestCase):
    def test_doctest(self):
        # pytest does not call the unittest load_tests hook, so a test method runs the examples.
        result = doctest.testmod(k3fnmatch)
        self.assertEqual(doctest.TestResults(failed=0, attempted=5), result)

    def test_doctest_pattern(self):
        # testmod(k3fnmatch) skips the functions that k3fnmatch.pattern defines.
        result = doctest.testmod(k3fnmatch.pattern)
        self.assertEqual(doctest.TestResults(failed=0, attempted=12), result)
