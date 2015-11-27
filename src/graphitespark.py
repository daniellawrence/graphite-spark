#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Written By Danny Lawrence <dannyla@linux.com>
#
#
from os import uname, popen
from sys import exit
from urllib2 import urlopen
import argparse
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
        '▁',
        '▂',
        '▃',
        '▄',
        '▅',
        '▆',
        '▇',
        '█'
    ]

    # The below takes all the data that has been gathered and finds the min and
    # max values for the list of data points. min() and max() where not used as
    # some times the data can contain a 'None' value.
    # This is also used to cast all the data into floats().
    for i in range(len(data)):
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

    for p in data:
        # work out the weighted value, as it can only be 0-7 as that is all we
        # can draw on the command line.
        weighted_value = int(round((p / max_point) * 7))
        six.print_(columns[weighted_value], end="")

    print(
        "\nMax: %(max_point)s\tMin: %(min_point)s\tFirst: %(first_point)s\
        \tLast: %(last_point)s\n" % locals())


def gather_data(url):
    """ use the url to gather the remote data from graphi via urllib2 """
    f = urlopen(url)
    all_data = f.readlines()
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


def hostname():
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
        "http://%(graphite_server)s/render?from=%(from_point)s"
        "&until=%(to_point)s&target=summarize(%(graph)s,'%(summarize_to)s',"
        "'%(summarize_by)s')&rawData=True") % locals()
    return url


def current_filesystem(filesystem='.'):
    """ Turn a requested path of a filesystem into the real filesystem. """
    real_filesystem = None
    # Assume solaris.
    df = 'df -h %(filesystem)s 2>&1' % locals()

    if uname()[0] == "Linux":
        df = 'df -Ph %(filesystem)s 2>&1' % locals()

    df_output = popen(df).readlines()
    try:
        real_filesystem = df_output[1].strip().split()[5].replace('/', '._')
    except IndexError:
        print("Couldn't find filesystem '%(filesystem)s' on this server" % locals())
        exit(1)
    return real_filesystem


def graph_filesystem(filesystem='.'):
    """ Given a filesystem generate the url to get its capacity """
    h = hostname()
    f = current_filesystem(filesystem)

    print("Filesystem capacity: %s" % (f.replace('._', '/')))

    graph = "systems.%(h)s.filesystem%(f)s.capacity" % locals()
    return graph


def graph_loadavg(la='15min'):
    """
    Generate the url for the load avg. for the current system (default: 15min )
    """
    h = hostname()
    graph = "systems.%(h)s.loadavg.%(la)s" % locals()
    return graph


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
        for la in ['1min', '5min', '15min']:
            graph = graph_loadavg(la)
            url = graph2url(graph)
            data = gather_data(url)
            draw_spark(data, title="%(la)s load avg." % locals())
        exit(0)

    if args.custom:
        url = graph2url(args.custom)
        data = gather_data(url)
        draw_spark(data)
        exit(0)

    return False


def main():
    """
    Parse the args, then bring on the sparks!
    """
    help_text = "Display a spark line of this or other servers"
    parser = argparse.ArgumentParser(description=help_text)
    parser.add_argument('-f', '--filesystem', metavar='filesystem', type=str)
    parser.add_argument('-l', '--loadavg', dest='loadavg', action='store_true')
    parser.add_argument('-c', '--custom', dest='custom',
                        metavar='custom graphite path', type=str)

    args = parser.parse_args()
    graphite_graph(args)
    parser.error('I dont know what you want to graph?')


if __name__ == "__main__":
    main()
