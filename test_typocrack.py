# -*- coding: utf-8 -*-
"""Unit tests for typocrack module."""
from unittest import TestCase

import typocrack as tc

pass1 = 'Hello'


class TestMutations(TestCase):
    def test_double(self):
        self.assertEqual(tc.double(pass1, 0), "HHello")
        self.assertEqual(tc.double(pass1, 1), "Heello")

    def test_drop(self):
        self.assertEqual(tc.drop(pass1, 1), "Hllo")

    def test_transpose(self):
        self.assertEqual(tc.transpose(pass1, 1), "Hlelo")
        # last index is a special case
        self.assertEqual(tc.transpose(pass1, 4), "Hello")

    def test_caseflip(self):
        self.assertEqual(tc.caseflip(pass1, 0), "hello")
        self.assertEqual(tc.caseflip(pass1, 1), "HEllo")


class TestCrackIntegration(TestCase):

    def test_simple_drop(self):
        target = 'Helo'
        phrase = tc.crack(pass1, tc.ALL, target.__eq__)
        self.assertEqual(target, phrase)

    def test_simple_caseflip(self):
        target = 'HellO'
        phrase = tc.crack(pass1, tc.ALL, target.__eq__)
        self.assertEqual(target, phrase)


if __name__ == '__main__': import unittest; unittest.main()