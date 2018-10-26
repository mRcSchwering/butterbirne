# This Python file uses the following encoding: utf-8
import unittest

from finData.stock import Stock


class MockDataloader(object):

    def getData(self, stock):
        return 'some data'


class MockFeatureExtractor(object):

    def getFeatures(self, stock):
        return 'some features'


class MockFeatureWriter(object):

    def writeFeatures(self, stock):
        return 'saved'


class Inits(unittest.TestCase):

    def test_nameSetIfProvided(self):
        s = Stock('isin', 'name')
        self.assertEqual('isin', s.isin)
        self.assertEqual('name', s.name)

    def test_isinAsName(self):
        s = Stock('isin')
        self.assertEqual('isin', s.isin)
        self.assertEqual('isin', s.name)


class DataDownload(unittest.TestCase):

    def test_dataDownloaded(self):
        s = Stock('isin')
        s.loadData(MockDataloader())
        self.assertEqual('some data', s.data)

    def test_wrongAdapter(self):
        s = Stock('isin')
        with self.assertRaises(AttributeError):
            s.loadData('asd')


class FeatureExtraction(unittest.TestCase):

    def test_featuresExtracted(self):
        s = Stock('isin')
        s.data = 'data'
        s.extractFeatures(MockFeatureExtractor())
        self.assertEqual('some features', s.features)

    def test_dataNotLoaded(self):
        s = Stock('isin')
        with self.assertRaises(AttributeError):
            s.extractFeatures('asd')


class FeatureSaving(unittest.TestCase):

    def test_featuresSaved(self):
        s = Stock('isin')
        s.features = 'features'
        res = s.saveFeatures(MockFeatureWriter())
        self.assertEqual('saved', res)

    def test_noFeaturesExtracted(self):
        s = Stock('isin')
        with self.assertRaises(AttributeError):
            s.saveFeatures(MockFeatureWriter())
