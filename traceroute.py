import time
from scapy.all import *
from ipwhois import IPWhois, IPDefinedError


class Traceroute:

    max_hops = 30
    __slots__ = {"hostname", "queries", "timeout", "ipv6", "verbose", "__dict__"}

    def __init__(self, hostname: str, queries=3, timeout=1000, ipv6=False, verbose=False):
        self.hostname = hostname
        self.queries = queries
        self.timeout = timeout
        self.ipv6 = ipv6
        self.verbose = verbose

    def traceroute(self) -> list[dict]:
        ans = []
        for i in range(1, self.max_hops + 1):
            pkt = self._create_packet(i)
            replies = self._send_packet(pkt)
            if len(replies) == 0:
                self._formatted_output(i, "*", "*", "     * ms")
                continue
            self._formatted_output(i, self._join_src(replies), self._get_asn(replies), self._get_times(replies))

            reply = replies[0]
            if reply.type != (3 if self.ipv6 else 11):
                print("Done!")
                break
        return ans

    def _send_packet(self, pkt: packet) -> list[packet]:
        answers = []
        for _ in range(self.queries):
            reply = sr1(pkt, verbose=0, timeout=self.timeout)
            if reply is not None:
                reply.reply_time = self._get_time(reply)
                answers.append(reply)
        return answers

    def _create_packet(self, cur_ttl: int) -> packet:
        if self.ipv6:
            return IPv6(dst=self.hostname, hlim=cur_ttl) / ICMPv6EchoRequest()
        return IP(dst=self.hostname, ttl=cur_ttl) / ICMP()

    @staticmethod
    def _get_time(reply: packet) -> int:
        seconds = time.time() - reply.time
        ms = seconds * 1000
        return ms

    @staticmethod
    def _formatted_output(n: int, ip: str, asn: str, ms: int) -> None:
        print(f'{n:<3}', f'{ip:<15}  ', f'{asn:<10}', ms)

    @staticmethod
    def _join_src(replies=list[packet]) -> str:
        return ' '.join(set([reply.src for reply in replies]))

    @staticmethod
    def _get_times(replies=list[packet]) -> float:
        times = [reply.reply_time for reply in replies]
        return '  '.join([f'{round(t, 3):>6} ms' for t in times])

    @staticmethod
    def _get_asn(replies=list[packet]) -> str:
        try:
            unique_ip = set([reply.src for reply in replies])
            return ' '.join([IPWhois(ip).ipasn.lookup()['asn'] for ip in unique_ip])
        except IPDefinedError:
            return 'Private'
