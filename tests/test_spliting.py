import unittest

import url2vapi


class TestSplit(unittest.TestCase):
    def test_split_all_ok(self):
        """Name: TestSplit.test_split_all_ok
        """
        parsed = url2vapi.split(
            'https://example.com:30/3.0/product/list?boom=1',
            pattern="<version:double>")

        self.assertEqual(parsed.version['value'], 3.0)
        self.assertEqual(parsed.remainder, 'product/list?boom=1')
        self.assertEqual(parsed.port, 30)
        self.assertEqual(parsed.domain, 'example.com')

        parsed = url2vapi.split(
            'https://example.com/3.14/product/list?boom=13.2',
            pattern="<version:double>")

        self.assertEqual(parsed.version['value'], 3.14)
        self.assertEqual(parsed.remainder, 'product/list?boom=13.2')
        self.assertEqual(parsed.port, None)
        self.assertEqual(parsed.domain, 'example.com')

    def test_split_errors(self):
        """Name: TestSplit.test_split_errors
        """
        with self.assertRaises(url2vapi.exceptions.UnrecognisedProtocol):
            url2vapi.split('ftp://example.com:30/3.0/product/list?boom=1')

    def test_more_complex_splitting(self):
        """Name: TestSplit.test_more_complex_splitting
        """
        parsed = url2vapi.split(
            'https://example.com/3.0/food_items/product/uid/1/?boom=1',
            pattern='<version:number>/<namespace>/')

        self.assertEqual(parsed.remainder, 'product/uid/1/?boom=1')
        self.assertEqual(parsed.domain, 'example.com')
        self.assertEqual(parsed.port, None)

        self.assertEqual(parsed.version['value'], 3)
        self.assertEqual(parsed.namespace['value'], 'food_items')

    def test_hard_fixed_url(self):
        """Name: TestSplit.test_hard_fixed_url

        Use case when we want to limit number of arguments on url.
        """
        parsed = url2vapi.split(
            'https://example.com/animal/lion/', pattern='/<key>/<value>/')

        self.assertEqual(parsed.remainder, '')
        self.assertEqual(parsed.domain, 'example.com')
        self.assertEqual(parsed.port, None)

        self.assertEqual(parsed.key['value'], 'animal')
        self.assertEqual(parsed.value['value'], 'lion')

        parsed = url2vapi.split(
            'https://example.com/animal/lion/ant/', pattern='<key>/<value>/')

        self.assertEqual(parsed.remainder, 'ant/')
        self.assertEqual(parsed.domain, 'example.com')
        self.assertEqual(parsed.port, None)

        self.assertEqual(parsed.key['value'], 'animal')
        self.assertEqual(parsed.value['value'], 'lion')

        parsed = url2vapi.split(
            'https://example.com/animal/lion/', pattern='<key>/<value>')

        self.assertEqual(parsed.remainder, '')
        self.assertEqual(parsed.domain, 'example.com')
        self.assertEqual(parsed.port, None)

        self.assertEqual(parsed.key['value'], 'animal')
        self.assertEqual(parsed.value['value'], 'lion')

    def test_hard_fixed_url_with_superflous_elements(self):
        """Name: TestSplit.test_hard_fixed_url_with_superflous_elements
        """
        parsed = url2vapi.split(
            'https://example.com/animal_feed/lion/meat/potato/ants/',
            pattern='/<key>/<value>/<value1>')

        self.assertEqual(parsed.remainder, 'potato/ants/')
        self.assertEqual(parsed.domain, 'example.com')
        self.assertEqual(parsed.port, None)

        self.assertEqual(parsed.key['value'], 'animal_feed')
        self.assertEqual(parsed.key['suffix'], '')
        self.assertEqual(parsed.key['prefix'], '')
        self.assertEqual(parsed.value['value'], 'lion')
        self.assertEqual(parsed.value['suffix'], '')
        self.assertEqual(parsed.value['prefix'], '')
        self.assertEqual(parsed.value1['value'], 'meat')
        self.assertEqual(parsed.value1['suffix'], '')
        self.assertEqual(parsed.value1['prefix'], '')

    def test_parsing_url_with_version_prefix(self):
        """Name: TestSplit.test_parsing_url_with_version_prefix
        """
        parsed = url2vapi.split(
            'https://example.com/v1.2.3-b1/animal_feed/lion/meat/potato/ants/',
            pattern='/v<version:tuple[double]:.>-b1/<namespace>/<...>')

        self.assertEqual(parsed.version['value'], (1, 2, 3))
        self.assertEqual(parsed.version['prefix'], 'v')
        self.assertEqual(parsed.version['suffix'], '-b1')
        self.assertEqual(parsed.namespace['value'], 'animal_feed')
        self.assertEqual(parsed.remainder, 'lion/meat/potato/ants/')
