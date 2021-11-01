import argparse
from traceroute import Traceroute


def main():
    p = argparse.ArgumentParser()
    p.add_argument('host', type=str, help='The host to traceroute to')
    p.add_argument('-s', '--sequence', type=int, default=0,
                   help='set sequence number for ICMP packets')
    p.add_argument('-q', '----queries', type=int, default=3,
                   help='Set the number of probes per each hop. Default is 3')
    p.add_argument('-z', '--sendwait', type=int, default=0,
                   help='Minimal time interval between probes (ms). Default is 0')
    p.add_argument('-w', '--wait', type=int, default=1000,
                   help='Wait for a probe no more than HERE (ms). Default is 1000')
    p.add_argument('-m', '--max-hops', type=int, default=30,
                   help='Set the max number of hops (max TTL to be reached). Default is 30')
    p.add_argument('--size', type=int, default=40,
                   help='Set packet size (bytes). Default is 40')

    args = p.parse_args()
    trace = Traceroute(args.host, args.sequence, args.queries, args.sendwait, args.wait, args.max_hops, args.size)
    trace.traceroute()


if __name__ == '__main__':
    main()
