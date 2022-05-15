import unittest
import logging

log = logging.getLogger(__name__)

class TestSample(unittest.TestCase):
    def test_example(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()