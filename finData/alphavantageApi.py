# This Python file uses the following encoding: utf-8
import requests
import json
import os

from finData.constants import Constants


class AlphavantagApi(object):

    _key = None
    _url = 'https://www.alphavantage.co/query'

    def __init__(self):
        self._key = self._configure_api()

    def request(self, paramsDict):
        """
        GET request to alphaVantag REST API

        provide params as dict key: value
        API reference: www.alphavantage.co/documentation
        """
        params = self._buildParamStrings(paramsDict)
        req = '{url}?{params}'.format(url=self._url, params='&'.join(params))
        res = self._GET(req)
        self._checkResponse(res)
        return self._getContent(res)

    def _buildParamStrings(self, paramsDict):
        paramsReq = ['function', 'symbol']
        paramsOpt = ['outputsize', 'datatype', 'interval']
        if not isinstance(paramsDict, dict):
            raise TypeError('Provide parameters as dictionary of key: value')
        for param in paramsReq:
            if param not in paramsDict.keys():
                raise KeyError('Parameter required: %s' % param)
        paramStrings = ['apikey=%s' % self._key]
        for key in paramsDict:
            if key not in paramsOpt + paramsReq:
                raise KeyError('Unused parameter: %s' % key)
            paramStrings.append('%s=%s' % (key, paramsDict[key]))
        return paramStrings

    @classmethod
    def _getContent(cls, res):
        content = json.loads(res.content.decode())
        try:
            contentKeys = content.keys()
        except AttributeError:
            raise AttributeError('Alpha Vantage returned empty content')
        if 'Error Message' in contentKeys:
            raise ValueError(content['Error Message'])
        return content

    @classmethod
    def _checkResponse(cls, res):
        if res.status_code != 200:
            raise AttributeError('Alpha Vantage returned: %s' % res.status_code)

    @classmethod
    def _GET(cls, url):
        return requests.get(url)

    @classmethod
    def _configure_api(cls):
        try:
            return os.environ['ALPHAVANTAGE_API_KEY']
        except KeyError:
            with open(Constants.configFilePath) as ouf:
                configFile = json.load(ouf)
            return configFile['ALPHAVANTAGE_API_KEY']
        raise KeyError('Alpha Vantage API Key not defined')
