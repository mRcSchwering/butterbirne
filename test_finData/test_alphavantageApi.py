# This Python file uses the following encoding: utf-8
import unittest
from unittest.mock import MagicMock

from finData.alphavantageApi import AlphavantagApi


def mockApi(response):

    class MockedAPI(AlphavantagApi):

        def _configure_api(cls):
            return 'xxx'

        def _GET(cls, url):
            return response

    return MockedAPI()


class AlphavantagApiSsetup(unittest.TestCase):

    def setUp(self):
        self.api = mockApi('test')

    def test_mockingApiKeyWorks(self):
        self.assertEqual(self.api._key, 'xxx')

    def test_mockingGetWorks(self):
        self.assertEqual(self.api._GET('asd'), 'test')


class BuildParamStrings(unittest.TestCase):

    def setUp(self):
        self.api = mockApi('')

    def test_noDictGiven(self):
        with self.assertRaises(TypeError):
            self.api._buildParamStrings('asd')

    def test_requiredParamsNotGiven(self):
        with self.assertRaises(KeyError):
            self.api._buildParamStrings({})
        with self.assertRaises(KeyError):
            self.api._buildParamStrings({'function': ''})

    def test_unusedOptParam(self):
        with self.assertRaises(KeyError):
            self.api._buildParamStrings({'function': '', 'symbol': '', 'opt': ''})

    def test_paramStringsWithOptParam(self):
        params = {'function': 'a', 'symbol': 'b', 'interval': 'c'}
        exp = set(['apikey=xxx', 'function=a', 'symbol=b', 'interval=c'])
        res = self.api._buildParamStrings(params)
        self.assertSetEqual(exp, set(res))


class StaticMethods(unittest.TestCase):

    def setUp(self):
        self.api = mockApi('')

    def test_non200response(self):
        resp = MagicMock()
        resp.status_code = 404
        with self.assertRaises(AttributeError):
            self.api._checkResponse(resp)

    def test_noKeysInResponse(self):
        resp = MagicMock()
        resp.status_code = 200
        resp.content.decode = MagicMock(return_value='[]')
        with self.assertRaises(AttributeError):
            self.api._getContent(resp)

    def test_errorMessageInResponse(self):
        resp = MagicMock()
        resp.status_code = 200
        resp.content.decode = MagicMock(return_value='{"Error Message": ""}')
        with self.assertRaises(ValueError):
            self.api._getContent(resp)


class Request(unittest.TestCase):

    def setUp(self):
        resp = MagicMock()
        resp.status_code = 200
        resp.content.decode = MagicMock(return_value='{"a": "test"}')
        self.api = mockApi(resp)

    def test_normalResponse(self):
        res = self.api.request({'function': '', 'symbol': ''})
        self.assertEqual('test', res['a'])
