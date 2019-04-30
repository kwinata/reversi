from unittest import TestCase

from interface import Interface, MyInput

tile_1 = '#'
tile_2 = '.'
tile_hint = '?'

class InterfaceTest(TestCase):

    def test_play(self):
        MyInput.args = [tile_1, "53", "64", "33", "quit"]
        Interface.main()
        scores = Interface.mainBoard.getPointBoard()
        self.assertEqual(4, scores[tile_1])
        self.assertEqual(6, scores[tile_2])
