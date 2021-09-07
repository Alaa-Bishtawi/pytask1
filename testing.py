import unittest

from models import Link


class TestLInk(unittest.TestCase):
    def test_boolean(self):
        OrginalUrl = "https://stackoverflow.com/questions/23944657/typeerror-method-takes-1-positional-argument-but-2-were-given"
        link = Link()
        b = link.isValidURL(OrginalUrl)
        a = True
        self.assertEqual(a, b)

    def test_string(self):
        OrginalUrl = "https://stackoverflow.com/questions/23944657/typeerror-method-takes-1-positional-argument-but-2-were-given"
        ShortUrl = "http://127.0.0.1:5000/616564bWiuut"
        a = len(ShortUrl)
        ShortUrl = ShortUrl[0:a - 6]
        link = Link()
        GeneratedShortendUrl = link.ShortenUrl(OrginalUrl)
        b = len(GeneratedShortendUrl)
        GeneratedShortendUrl = link.server_url + GeneratedShortendUrl[0:b - 6]
        self.assertEqual(ShortUrl, GeneratedShortendUrl)


if __name__ == '__main__':
    unittest.main()
