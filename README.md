# Traceroute

```
usage: main.py [-h] [-s SEQUENCE] [-q QUERIES] [-z SENDWAIT] [-w WAIT] [-m MAX_HOPS] [--size SIZE] host

positional arguments:
  host                  The host to traceroute to

options:
  -h, --help            show this help message and exit
  -s SEQUENCE, --sequence SEQUENCE
                        set sequence number for ICMP packets
  -q QUERIES, ----queries QUERIES
                        Set the number of probes per each hop. Default is 3
  -z SENDWAIT, --sendwait SENDWAIT
                        Minimal time interval between probes (ms). Default is 0
  -w WAIT, --wait WAIT  Wait for a probe no more than HERE (ms). Default is 1000
  -m MAX_HOPS, --max-hops MAX_HOPS
                        Set the max number of hops (max TTL to be reached). Default is 30
  --size SIZE           Set packet size (bytes). Default is 40
```