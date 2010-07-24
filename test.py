#-*- coding: utf-8 -*-
import os
from unittest import TestCase

from api import Forvo

FORVO_API_KEY = os.getenv('FORVO_API_KEY')

class ForvoTest(TestCase):
    def test_pronunctation(self):
        f = Forvo(FORVO_API_KEY)
        f.pronounce('testing')
    
    def _test_utf8_word(self):
        f = Forvo(FORVO_API_KEY)
        f.pronounce('exámen')
