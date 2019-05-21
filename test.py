from unittest import TestCase

from rule import Rule
from interface import Interface, MyInput
from manager import Manager

tile_1 = '#'
tile_2 = '.'
tile_hint = '?'


class InterfaceTest(TestCase):

    def play(self, args, expPlayerScore, expComputerScore):
        MyInput.args = args
        Manager.main()
        scores = Rule.getPointBoard(Interface.mainBoard)
        self.assertEqual(expPlayerScore, scores[tile_1])
        self.assertEqual(expComputerScore, scores[tile_2])

    def test_play(self):
        self.play([tile_1, "53", "64", "33", "quit"], 4, 6)
        self.play([tile_1, "35", "37", "88", "63", "27", "18", "quit"], 6, 8)
        self.play(["53", tile_1, "53", "cat", "quit"], 3, 3)
