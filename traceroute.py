from scapy import packet
from scapy.sendrecv import sr1
from scapy.layers.inet import IP, ICMP
from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest
from ipwhois import IPWhois, IPDefinedError


class Traceroute:

    max_hops = 30
    __slots__ = {"hostname", "queries", "timeout", "ipv6", "verbose", "__dict__"}

    def __init__(self, hostname: str, queries=3, timeout=1.0, ipv6=False, verbose=False):
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
                self._formatted_output(i, "*", "     * ms", "*" if self.verbose else None)
                continue
            asn = self._get_asn(replies) if self.verbose else None
            self._formatted_output(i, self._join_src(replies), self._get_times(replies), asn)

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
                reply.reply_time = reply.time - pkt.sent_time
                answers.append(reply)
        return answers

    def _create_packet(self, cur_ttl: int) -> packet:
        if self.ipv6:
            return IPv6(dst=self.hostname, hlim=cur_ttl) / ICMPv6EchoRequest()
        return IP(dst=self.hostname, ttl=cur_ttl) / ICMP()

    def _formatted_output(self, n: int, ip: str, ms: str, asn: str = None) -> None:
        if asn is not None:
            print(f'{n:<3}', f'{ip:<15}  ', format(ms, '<' + str(self.queries * 10 + 1)), asn)
        else:
            print(f'{n:<3}', f'{ip:<15}  ', ms)

    @staticmethod
    def _join_src(replies: list[packet]) -> str:
        return ' '.join(set([reply.src for reply in replies]))

    @staticmethod
    def _get_times(replies: list[packet]) -> str:
        times = [reply.reply_time for reply in replies]
        return '  '.join([f'{round(t, 3):>6} ms' for t in times])

    @staticmethod
    def _get_asn(replies: list[packet]) -> str:
        try:
            unique_ip = set([reply.src for reply in replies])
            return ' '.join([IPWhois(ip).ipasn.lookup()['asn'] for ip in unique_ip])
        except IPDefinedError:
            return 'Private'
