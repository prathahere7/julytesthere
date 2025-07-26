import unittest
from api.helpers import unsafe_query

class TestHelpers(unittest.TestCase):

    def test_query(self):
        result = unsafe_query("admin' --")
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()
