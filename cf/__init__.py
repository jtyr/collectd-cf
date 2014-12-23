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

        request = urllib2.Request(url)
        request.add_header('Referer', 'https://www.currencyfair.com/')
        response = urllib2.urlopen(request)
        content = response.read()
        data = json.loads(content)

        ret = {}

        if 'calculator' in data:
            if 'ALL' in keys:
                for ckey in data['calculator']:
                    ret[ckey] = data['calculator'][ckey]
            else:
                for key in keys:
                    if key in data['calculator']:
                        ret[key] = data['calculator'][key]
                    else:
                        ret[key] = None

        return ret
