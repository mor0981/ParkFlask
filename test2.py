import unittest


class TestHello(unittest.TestCase):
    def test_setUp(self):
        self.assertTrue(True)
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()