# This Python file uses the following encoding: utf-8


class Constants(object):

    configFilePath = 'config.json'

    columnConversions = {
        'alphavantage': [
            {"from": "open", "to": "open"},
            {"from": "high", "to": "high"},
            {"from": "low", "to": "low"},
            {"from": "close", "to": "close"},
            {"from": "adjusted close", "to": "adj_close"},
            {"from": "volume", "to": "volume"},
            {"from": "dividend amount", "to": "divid_amt"},
            {"from": "split coefficient", "to": "split_coef"}
        ]
    }
