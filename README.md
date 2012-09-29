graphite-spark
==============

A sparkline for graphite data:  ▄ ▄ ▆ ▇ ▄ ▄ ▃ ▃

When to use
-----------

Its 3am you have just ssh'd to a server and due to performance problems.
The Load seems high, but you look after 2000 servers... Is this a normal load?
You need to know what is ''high'' for this system????

A quick ''' spark.py -l ''' and you can see a 24 hour history of the loadavg
for this system.

You know now that is a normal loadavg and you can investigate somethng else.

Usage
------

usage: spark.py [-h] [-f filesystem] [-l] [-c custom graphite path]

Display a sparkline of this or other servers

optional arguments:
    -h, --help            show this help message and exit
    -f filesystem, --filesystem filesystem
    -l, --loadavg
    -c custom graphite path, --custom custom graphite path



Example - Check Load average
-----------------------------

Checking the load averages of the current system that you are logged into
straigh from the command line!

    server 1 % spark.py -l
    -24hours@1h blocks
    1min load avg.
    █ ▅ ▆ ▄ ▄ ▆ ▆ ▄ ▃ ▃ ▃ ▂ ▃ ▃ ▂ ▃ ▃ ▃ ▃ ▃ ▄ ▅ ▃ ▃ 
    Max: 2.95       Min: 0.6        First: 2.95     Last: 0.82

    -24hours@1h blocks
    5min load avg.
    █ ▄ ▄ ▄ ▄ ▆ ▇ ▄ ▄ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ 
    Max: 2.26       Min: 0.54       First: 2.26     Last: 0.76

    -24hours@1h blocks
    15min load avg.
    █ ▆ ▄ ▄ ▅ ▇ ▇ ▆ ▄ ▄ ▄ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ ▃ 
    Max: 1.82       Min: 0.53       First: 1.82     Last: 0.59

Example - filesystem capcity
-----------------------------

Checking the the filesystem capacity of a local filesystem on the current host,
from the data in a remote graphite server.

    server 1 % ./spark.py -f /var/tmp
    Filesystem capacity: /var
    -24hours@1h blocks
    █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ 
    Max: 11.0       Min: 11.0       First: 11.0     Last: 11.0

As you can see the script was able to work out the mount point of the filesystem
so that the data was still found in the graphite system.

Example - custom graphs
-----------------------------

Checking anything that you want from any system that you are logged into.
As the data is in the remote graphite system.

    server 1 % ./spark.py -c 'systems.s.server2.loadavg.15min'
    -24hours@1h blocks
    ▅ ▅ ▅ ▄ █ █ ▅ ▄ ▂ ▄ ▃ ▂ ▂ ▂ ▂ ▂ ▂ ▂ ▃ ▃ ▃ ▂ ▃ ▂ ▂ 
    Max: 15.03      Min: 1.73       First: 9.07     Last: 1.73
