import unittest
import main

class TestCano(unittest.TestCase):

    def test_toLowerCase(self):
        result = main.canonicalization("HTTP://www.Example.com/SomeFile.html")
        self.assertEqual(result, "http://www.example.com/somefile.html")

    def test_port(self):
        result = main.canonicalization("HTTP://www.Example.com/SomeFile.html:80")
        self.assertEqual(result, "http://www.example.com/somefile.html")

    def test_fragment(self):
        result = main.canonicalization("HTTP://www.Example.com/SomeFile.html#contact")
        self.assertEqual(result, "http://www.example.com/somefile.html")

    def test_doubleBackSlash(self):
        result = main.canonicalization("HTTP://www.Example.com//SomeFile.html#contact")
        self.assertEqual(result, "http://www.example.com/somefile.html")