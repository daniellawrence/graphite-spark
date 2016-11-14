#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Written By Danny Lawrence <dannyla@linux.com>
"""

from os import uname, popen
from urllib2 import urlopen
import six


def draw_spark(data=None, max_point=-1, min_point=65333, title=None):
    """ Draw the sparkline based on the list of data points
    The column that will be used for each point is the datapoint as a float()
    diveded by the value of the point with the highest value (maximum).
    This is then Rounded to the nearest whole number, then the total is
    mutlplied by 7. This weighted number is then used as the index to the below
    list. Where the max value would be index 7 (█) and the least value
    would be index 0 (▁)
    """
    columns = [
        '▁', '▂', '▃', '▄',
        '▅', '▆', '▇', '█'
    ]

    # The below takes all the data that has been gathered and finds the min and
    # max values for the list of data points. min() and max() where not used as
    # some times the data can contain a 'None' value.
    # This is also used to cast all the data into floats().
    for i, _ in enumerate(data):
        try:
            data[i] = float(data[i])
        except ValueError:
            del data[i]
            continue

        if data[i] > max_point:
            max_point = data[i]
        if data[i] < min_point:
            min_point = data[i]

    # Get the first and last datapoint to be used in the display of the spark.
    first_point = data[0]
    last_point = data[-1]

    # If we have title then print it out
    if title:
        print(title)

    for point in data:
        # work out the weighted value, as it can only be 0-7 as that is all we
        # can draw on the command line.
        weighted_value = int(round((point / max_point) * 7))
        six.print_(columns[weighted_value], end="")

    print("Max: {0} min: {1} First: {2} Last: {3}".format(
        max_point, min_point, first_point, last_point
    ))


def gather_data(url):
    """ use the url to gather the remote data from graphi via urllib2 """
    file_handle = urlopen(url)
    all_data = file_handle.readlines()

    try:
        data = all_data[0]
    except IndexError:
        print("The url='%(url)s'\nDid not return any data.." % locals())
        exit(1)

    if '|' not in data:
        print("The url='%(url)s'\nDid not return correct data..." % locals())
        exit(1)
    data = data.split('|')[1].split(',')
    return data


def get_hostname():
    """ Work out the current hostname """
    host = uname()[1]
    return "%s.%s" % (host[0], host)


def graph2url(graph):
    """
    take a desired graph and turn it in to the graphite url-api expected format.
    This will be used to allow for different time ranges and summearized values.
    eg.
        >>> graph2url('systems.h.hostname.loadavg.15min')
        http://graphite/render?from=-28hours&until=now&target=summarize( \
        "systems.h.hostname.loadavg.15min","1h","max")&rawData=True
    """
    graphite_server = "graphite"
    from_point = "-24hours"
    to_point = "now"
    summarize_to = "1h"
    summarize_by = "max"

    print("%(from_point)s@%(summarize_to)s blocks" % locals())

    url = (
        "http://{graphite_server}/render?from={from_point}"
        "&until={to_point}&target=summarize({graph},'{summarize_to}',"
        "'{summarize_by}')&rawData=True"
    ).format(
        graphite_server=graphite_server, from_point=from_point,
        to_point=to_point, graph=graph, summarize_to=summarize_to,
        summarize_by=summarize_by
    )

    return url


def get_current_filesystem(filesystem='.'):
    """ Turn a requested path of a filesystem into the real filesystem. """
    real_filesystem = None
    # Assume solaris.
    df_command = 'df -h {0} 2>&1'.format(filesystem)

    if uname()[0] == "Linux":
        df_command = 'df -Ph {0} 2>&1'.format(filesystem)

    df_output = popen(df_command).readlines()
    try:
        real_filesystem = df_output[1].strip().split()[5].replace('/', '._')
    except IndexError:
        print("Couldn't find filesystem '%(filesystem)s' on this server" % locals())
        exit(1)
    return real_filesystem


def graph_filesystem(filesystem='.'):
    """ Given a filesystem generate the url to get its capacity """
    hostname = get_hostname()
    current_filesystem = get_current_filesystem(filesystem)

    print("Filesystem capacity: %s" % (current_filesystem.replace('._', '/')))

    return "systems.{0}.filesystem{1}.capacity".format(hostname, current_filesystem)


def graph_loadavg(load_avg='15min'):
    """
    Generate the url for the load avg. for the current system (default: 15min )
    """
    hostname = get_hostname()
    return "systems.{0}.loadavg.{1}".format(hostname, load_avg)


def graphite_graph(args):
    """ Depending on the args that have been given, show the user diffrent sparks.
    If the user didn't choose a spark line return false, so that the usage
    can be shown instead.
    """
    url = None

    if args.filesystem:
        graph = graph_filesystem(filesystem=args.filesystem)
        url = graph2url(graph)
        data = gather_data(url)
        draw_spark(data)
        exit(0)

    if args.loadavg:
        for load_avg in ['1min', '5min', '15min']:
            graph = graph_loadavg(load_avg)
            url = graph2url(graph)
            data = gather_data(url)
            draw_spark(data, title="{0} load avg.".format(load_avg))
        exit(0)

    if args.custom:
        url = graph2url(args.custom)
        data = gather_data(url)
        draw_spark(data)
        exit(0)

    return False
