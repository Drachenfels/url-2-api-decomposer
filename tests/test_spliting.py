import unittest

import url4api


class TestSplit(unittest.TestCase):
    def test_split_all_ok(self):
        """Name: TestSplit.test_split_all_ok
        """
        processed = url4api.split(
            'https://example.com:30/3.0/product/list?boom=1')

        self.assertEqual(processed.version, 3.0)
        self.assertEqual(processed.url, 'product/list?boom=1')
        self.assertEqual(processed.port, 30)
        self.assertEqual(processed.domain, 'example.com')

        processed = url4api.split(
            'https://example.com/3.14/product/list?boom=13.2')

        self.assertEqual(processed.version, 3.14)
        self.assertEqual(processed.url, 'product/list?boom=13.2')
        self.assertEqual(processed.port, None)
        self.assertEqual(processed.domain, 'example.com')

    def test_split_errors(self):
        """Name: TestSplit.test_split_errors
        """
        with self.assertRaises(url4api.exceptions.UnrecognisedProtocol):
            url4api.split('ftp://example.com:30/3.0/product/list?boom=1')
