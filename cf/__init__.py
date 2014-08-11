import json
import urllib2


class CurrencyFair():
    def __init__(self, frm, to, amount, direction='SELL'):
        self.frm = frm
        self.to = to
        self.amount = amount
        self.direction = direction

    def get_data(self, keys=['cfRate']):
        url = (
            'https://app.currencyfair.com/api/fleece?'
            'currencyfrom=%s&'
            'currencyto=%s&'
            'amount=%s&'
            'buysell=%s' %
            (self.frm, self.to, self.amount, self.direction))

        response = urllib2.urlopen(url)
        content = response.read()
        data = json.loads(content)

        ret = {}

        if 'calculator' in data:
            for key in keys:
                if key in data['calculator']:
                    ret[key] = data['calculator'][key]
                else:
                    ret[key] = None

        return ret
