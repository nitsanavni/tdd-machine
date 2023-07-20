import unittest

class TestChat(unittest.TestCase):

    def test_infer_chatter(self):
        self.assertEqual(infer_chatter(), 'Unknown')

if __name__ == '__main__':
    unittest.main()
