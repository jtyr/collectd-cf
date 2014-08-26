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


Tools
-----

There is also a command line tool which allows to test the configuration parameters:

```
$ ./cf.py --help
usage: cf.py [-h] -f STR -t STR -a NUM [-d STR] [-k STR] [-v]

Reads currency rates from CyrrenciFair.

optional arguments:
  -h, --help            show this help message and exit
  -f STR, --from STR    from currency (e.g. GBP)
  -t STR, --to STR      to currency (e.g. CZK)
  -a NUM, --amount NUM  amount (e.g. 1000)
  -d STR, --direction STR
                        buy or sell (default: SELL)
  -k STR, --keys STR    list of keys from the JSON message separated by comma.
                        Use ALL to show all keys. (default: cfRate)
  -v, --verbose         verbose output
```

Example of usage is as follows:

```
$ ./cf.py --from GBP --to CZK --amount 1000 --direction SELL
cfRate: 34.66
```


Dependencies
------------

- `urllib2`


Sources
-------

- http://collectd.org/documentation/manpages/collectd-python.5.shtml


Author
------

Jiri Tyr <jiri.tyr@gmail.com>
