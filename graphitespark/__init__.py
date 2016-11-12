import argparse

from graphitespark import graphite_graph


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
