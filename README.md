# Traceroute

```
usage: main.py [-h] [-t TIMEOUT] [-n N] [-v] [-6] ip_address

positional arguments:
  ip_address            target ip address

options:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout waiting for a response (s). Default is 2
  -n N                  Set the number of probes per each hop. Default is 3
  -v, --verbose         Verbose mode
  -6                    Use IPv6
```