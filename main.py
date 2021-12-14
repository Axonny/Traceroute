import argparse
from traceroute import Traceroute


def main():
    p = argparse.ArgumentParser()
    p.add_argument('ip_address', type=str, help='target ip address')
    p.add_argument('-t', '--timeout', type=float, default=2, help='Timeout waiting for a response (s). Default is 2')
    p.add_argument('-n', type=int, default=3, help='Set the number of probes per each hop. Default is 3')
    p.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    p.add_argument('-6', action='store_true', help='Use IPv6', dest='ipv6')

    args = p.parse_args()

    trace = Traceroute(args.ip_address, args.n, args.timeout, args.ipv6, args.verbose)
    trace.traceroute()


if __name__ == '__main__':
    main()
