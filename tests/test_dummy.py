import unittest

class DummyTest(unittest.TestCase):
  def test_function(self):
    self.assertEqual(1,1)

if __name__ == '__main__':
  unittest.main()