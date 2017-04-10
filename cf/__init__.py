import json

try:
    from urllib2 import Request
    from urllib2 import urlopen
except ImportError:
    from urllib.request import Request
    from urllib.request import urlopen


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

        request = Request(url)
        request.add_header('Referer', 'https://www.currencyfair.com/')
        response = urlopen(request)
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
