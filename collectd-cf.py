#!/usr/bin/env python


import collectd
from cf import CurrencyFair


class CollectdCF():
    def __init__(self):
        self.message('I', 'Class init...')
        self.DATA = []
        self.INTERVAL = 0

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
        self.message('I', 'Configuring callback...')

        for node in conf.children:
            if len(node.values) == 5:
                record = {
                    'label': node.key,
                    'from': node.values[0],
                    'to': node.values[1],
                    'amount': node.values[2],
                    'direction': node.values[3],
                    'reciprocal': node.values[4],
                }

                self.DATA.append(record)
            elif node.key == 'Interval':
                self.INTERVAL = int(node.values[0])

        self.message('I', "Data: %s" % str(self.DATA))
        self.message('I', "Interval: %s" % (
            self.INTERVAL if self.INTERVAL > 0 else 'default'))

        # Register the read callback to be able to set the correct interval
        collectd.register_read(self.read_callback, interval=self.INTERVAL)

    def read_callback(self, data=None):
        self.message('I', 'Reader callback...')

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
            metric.plugin = 'currencyfair'
            metric.plugin_instance = record['label']
            metric.type = 'gauge'
            metric.type_instance = 'cfrate'
            metric.values = [value]
            metric.dispatch()


# Create a new instance of the plugin
collecd_cf = CollectdCF()

# Register config callback which will register the read callback
collectd.register_config(collecd_cf.configure_callback)
