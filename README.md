Collectd CurrencyFair plugin
=============================

Description
-----------

This is a Collectd plugin which allows you to monitor currency rates provided
by [CurrencyFair](http://www.currencyfair.com).


Configuration
-------------

Configuration is done in the `/etc/collectd.conf` file.

Enable python plugin:

```
<LoadPlugin python>
    Globals true
</LoadPlugin>
```

Configure the CurrencyFair plugin:

```
<Plugin "python">
    ModulePath "/path/to/your/collectd-cf"
    LogTraces true
    Interactive false
    Import "collectd-cf"

    <Module "collectd-cf">
        # Label  From  To    Amount  Dir    Reciprocal
        GBPCZK  "GBP" "CZK" "1000"  "SELL" "NO"
        # Here you can specify even more currencies:
        #CZKGBP  "CZK" "GBP" "1000"  "SELL" "YES"
    </Module>
</Plugin>
```

Restart the `collectd` daemon and it should work.


Dependencies
------------

- `urllib2`


Sources
-------

- http://collectd.org/documentation/manpages/collectd-python.5.shtml


Author
------

Jiri Tyr <jiri.tyr@gmail.com>