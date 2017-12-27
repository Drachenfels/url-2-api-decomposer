import unittest

import url4api


class TestSplit(unittest.TestCase):
    def test_split_all_ok(self):
        """Name: TestSplit.test_split_all_ok
        """
        processed = url4api.split(
            'https://example.com:30/3.0/product/list?boom=1',
            pattern="<version:double>/<...>")

        self.assertEqual(processed.version, 3.0)
        self.assertEqual(processed.url, 'product/list?boom=1')
        self.assertEqual(processed.port, 30)
        self.assertEqual(processed.domain, 'example.com')

        processed = url4api.split(
            'https://example.com/3.14/product/list?boom=13.2',
            pattern="<version:double>/<...>")

        self.assertEqual(processed.version, 3.14)
        self.assertEqual(processed.url, 'product/list?boom=13.2')
        self.assertEqual(processed.port, None)
        self.assertEqual(processed.domain, 'example.com')

    def test_split_errors(self):
        """Name: TestSplit.test_split_errors
        """
        with self.assertRaises(url4api.exceptions.UnrecognisedProtocol):
            url4api.split('ftp://example.com:30/3.0/product/list?boom=1')

    def test_more_complex_splitting(self):
        """Name: TestSplit.test_more_complex_splitting
        """
        processed = url4api.split(
            'https://example.com/3.0/food_items/product/uid/1/?boom=1',
            pattern='<version:number>/<namespace>/<...>')

        self.assertEqual(processed.url, 'product/uid/1/?boom=1')
        self.assertEqual(processed.domain, 'example.com')
        self.assertEqual(processed.port, None)

        self.assertEqual(processed.version, 3)
        self.assertEqual(processed.namespace, 'food_items')

    def test_hard_fixed_url(self):
        """Name: TestSplit.test_hard_fixed_url_

        Use case when we want to limit number of arguments on url.
        """
        processed = url4api.split(
            'https://example.com/animal/lion/', pattern='/<key>/<value>/')

        self.assertEqual(processed.url, '')
        self.assertEqual(processed.domain, 'example.com')
        self.assertEqual(processed.port, None)

        self.assertEqual(processed.key, 'animal')
        self.assertEqual(processed.value, 'lion')

        processed = url4api.split(
            'https://example.com/animal/lion/', pattern='<key>/<value>/')

        self.assertEqual(processed.url, '')
        self.assertEqual(processed.domain, 'example.com')
        self.assertEqual(processed.port, None)

        self.assertEqual(processed.key, 'animal')
        self.assertEqual(processed.value, 'lion')

        processed = url4api.split(
            'https://example.com/animal/lion/', pattern='<key>/<value>')

        self.assertEqual(processed.url, '')
        self.assertEqual(processed.domain, 'example.com')
        self.assertEqual(processed.port, None)

        self.assertEqual(processed.key, 'animal')
        self.assertEqual(processed.value, 'lion')

    def test_hard_fixed_url_with_superflous_elements(self):
        """Name: TestSplit.test_hard_fixed_url_with_superflous_elements
        """
        processed = url4api.split(
            'https://example.com/animal_feed/lion/meat/potato/ants/',
            pattern='/<key>/<value>/<value1>')

        self.assertEqual(processed.url, '')
        self.assertEqual(processed.domain, 'example.com')
        self.assertEqual(processed.port, None)

        self.assertEqual(processed.key, 'animal_feed')
        self.assertEqual(processed.value, 'lion')
        self.assertEqual(processed.value1, 'meat')

    def test_argparse_in_wrong_place(self):
        """Name: TestSplit.test_argparse_in_wrong_place
        """
        with self.assertRaises(url4api.exceptions.InvalidInputPattern):
            processed = url4api.split(
                'https://example.com/animal_feed/lion/meat/potato/ants/',
                pattern='/<key>/<...>/<value>/<value1>')
