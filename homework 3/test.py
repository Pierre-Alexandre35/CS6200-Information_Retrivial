import unittest
import main

class TestCano(unittest.TestCase):

    def test_toLowerCase(self):
        result = main.canonicalization("HTTP://www.Example.com/SomeFile.html")
        self.assertEqual(result, "http://www.example.com/somefile.html")

    def test_Port(self):
        result = main.canonicalization("HTTP://www.Example.com/SomeFile.html:80")
        self.assertEqual(result, "http://www.example.com/somefile.html")

    def test_Fragment(self):
        result = main.canonicalization("HTTP://www.Example.com/SomeFile.html#contact")
        self.assertEqual(result, "http://www.example.com/somefile.html")
