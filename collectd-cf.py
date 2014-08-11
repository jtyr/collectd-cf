#!/usr/bin/env python


import collectd
from cf import CurrencyFair


class CollectdCF():
    def __init__(self):
        self.message('I', 'Class init stuff...')
        self.DATA = []

    def message(self, level, text):
        text = '%s: %s' % (level, text)

        if level == 'E':
            collectd.error(text)
        elif level == 'W':
            collectd.warning(text)
        elif level == 'N':
            collectd.notice(text)
        elif level == 'I':
            collectd.info(text)
        else:
            collectd.debug(text)

    def configure_callback(self, conf):
        self.message('I', 'Configuring stuff...')

        for node in conf.children:
            record = {
                'label': node.key,
                'from': node.values[0],
                'to': node.values[1],
                'amount': node.values[2],
                'direction': node.values[3],
                'reciprocal': node.values[4],
            }

            self.DATA.append(record)

        self.message('I', str(self.DATA))

    def read_callback(self, data=None):
        self.message('I', 'Reader stuff...')

        for record in self.DATA:
            cf = CurrencyFair(
                record['from'],
                record['to'],
                record['amount'],
                record['direction'])

            values = None

            try:
                values = cf.get_data()
            except Exception as e:
                self.message('I', 'Can not get data: %s' % (e))
                break

            value = values['cfRate']
            if record['reciprocal'] == 'YES':
                value = "%0.4f" % (1 / float(value))

            self.message('I', "cfRate=%s (%s)" % (value, record['label']))

            metric = collectd.Values()
            metric.plugin = 'python-currencyfair'
            metric.plugin_instance = record['label']
            metric.type = 'gauge'
            metric.type_instance = 'cfrate'
            metric.values = [value]
            metric.dispatch()


# Create a new instance of the plugin
collecd_cf = CollectdCF()

# register callbacks
collectd.register_config(collecd_cf.configure_callback)
collectd.register_read(collecd_cf.read_callback)
