# https://docs.python.org/3/library/unittest.html

import unittest
import util


class TestUtil(unittest.TestCase):

    def test_01(self):
        msg = "Como este é o nosso primeiro contato, eu gostaria de me apresentar pra você."
        self.assertEqual(util.quebralinha(msg), "Como este é o nosso primeiro contato, eu gostaria de me apresentar pra você.")